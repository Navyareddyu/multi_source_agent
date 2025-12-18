import streamlit as st
import sqlite3
import os

# --- CRITICAL FIX: Use the dedicated Ollama package ---
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from langchain_core.tools import tool
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# --- 1. TOOL DEFINITIONS (Same as before) ---
@tool
def document_search(query: str) -> str:
    """Searches company policy documents for answers about strategy or rules."""
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
    docs = vectorstore.similarity_search(query, k=2)
    return "\n---\n".join([d.page_content for d in docs])

@tool
def run_sql_query(query: str) -> str:
    """Executes SQL on the company_records table for facts/figures."""
    try:
        conn = sqlite3.connect("agent_data.db")
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return f"Database Results: {results}"
    except Exception as e:
        return f"SQL Error: {e}"

tools = [document_search, run_sql_query]
tools_map = {t.name: t for t in tools}

# --- 2. INITIALIZE LLM (Now using bind_tools correctly) ---
# Ensure you are using a tool-capable model like mistral or llama3.1
llm = ChatOllama(model="mistral", temperature=0).bind_tools(tools)

# --- 3. STREAMLIT UI ---
st.title("🤖 Modern AI Agent (No AgentExecutor)")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    # Skip raw tool messages in UI display for clarity
    if not isinstance(msg, ToolMessage):
        with st.chat_message(role):
            st.markdown(msg.content)

# Chat logic
if prompt := st.chat_input("Ask about revenue or policies"):
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Step A: Get LLM response
            response = llm.invoke(st.session_state.messages)
            
            # Step B: If LLM wants to use tools, execute them
            while response.tool_calls:
                st.session_state.messages.append(response)
                
                for tool_call in response.tool_calls:
                    # Run the requested tool
                    tool_to_call = tools_map[tool_call["name"]]
                    tool_result = tool_to_call.invoke(tool_call["args"])
                    
                    # Show tool usage status in Streamlit
                    with st.status(f"Running {tool_call['name']}...", expanded=False):
                        st.write(f"Query: {tool_call['args']}")
                        st.write(f"Result: {tool_result}")
                    
                    # Add tool result back to history
                    st.session_state.messages.append(
                        ToolMessage(content=str(tool_result), tool_call_id=tool_call["id"])
                    )
                
                # Step C: Ask LLM again with the new tool data
                response = llm.invoke(st.session_state.messages)

            # Final answer display
            st.markdown(response.content)
            st.session_state.messages.append(response)