# agent.py - Simple Multi-Source Knowledge Agent

from langchain_community.chat_models import ChatOllama
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
import sqlite3
import re

# -------------------------
# 1. RAG Function
# -------------------------
def document_search(query: str) -> str:
    """Search through company documents and policies for information."""
    try:
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
        docs = vectorstore.similarity_search(query, k=2)
        context = "\n---\n".join([d.page_content for d in docs])
        return f"Retrieved Context:\n{context}"
    except Exception as e:
        return f"Document search error: {e}"

# -------------------------
# 2. SQL Function
# -------------------------
def run_sql_query(query: str) -> str:
    """Execute SQL queries on the company database."""
    try:
        conn = sqlite3.connect("agent_data.db")
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        schema = "company_records(metric TEXT, value REAL, unit TEXT, quarter TEXT)"
        return f"Schema: {schema}\nResults: {results}"
    except Exception as e:
        return f"SQL Error: {e}"

# -------------------------
# 3. LLM Setup
# -------------------------
llm = ChatOllama(model="mistral", base_url="http://localhost:11434", temperature=0.0)

# -------------------------
# 4. Simple Agent Logic
# -------------------------
def run_agent(question: str):
    print(f"\nUSER: {question}")
    
    # Determine which tool to use based on keywords
    question_lower = question.lower()
    
    context = ""
    
    # Check if it's a SQL-type question
    if any(word in question_lower for word in ['revenue', 'profit', 'q1', 'q2', 'q3', 'q4', 'quarter', 'employees', 'value', 'metric']):
        print("Using SQL database...")
        # Generate appropriate SQL query
        if 'revenue' in question_lower:
            if 'q1' in question_lower:
                sql_result = run_sql_query("SELECT * FROM company_records WHERE metric='Revenue' AND quarter='Q1'")
            elif 'q2' in question_lower:
                sql_result = run_sql_query("SELECT * FROM company_records WHERE metric='Revenue' AND quarter='Q2'")
            else:
                sql_result = run_sql_query("SELECT * FROM company_records WHERE metric='Revenue'")
        elif 'profit' in question_lower:
            if 'q1' in question_lower:
                sql_result = run_sql_query("SELECT * FROM company_records WHERE metric='Profit' AND quarter='Q1'")
            elif 'q2' in question_lower:
                sql_result = run_sql_query("SELECT * FROM company_records WHERE metric='Profit' AND quarter='Q2'")
            else:
                sql_result = run_sql_query("SELECT * FROM company_records WHERE metric='Profit'")
        elif 'employees' in question_lower:
            sql_result = run_sql_query("SELECT * FROM company_records WHERE metric='Total Employees'")
        else:
            sql_result = run_sql_query("SELECT * FROM company_records")
        
        context = f"Database Results: {sql_result}"
    
    # Check if it's a document search question
    elif any(word in question_lower for word in ['policy', 'remote', 'work', 'strategy', 'phoenix', 'document']):
        print("Using document search...")
        doc_result = document_search(question)
        context = f"Document Search Results: {doc_result}"
    
    # If no specific tool needed, search both
    else:
        print("Searching both sources...")
        doc_result = document_search(question)
        sql_result = run_sql_query("SELECT * FROM company_records LIMIT 5")
        context = f"Document Results: {doc_result}\n\nDatabase Results: {sql_result}"
    
    # Create prompt for LLM
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Answer the user's question based on the provided context. Be concise and accurate."),
        ("human", f"Question: {question}\n\nContext: {context}\n\nAnswer:")
    ])
    
    # Get response from LLM
    chain = prompt | llm
    response = chain.invoke({"question": question, "context": context})
    
    print(f"\nAGENT ANSWER:\n{response.content}")
    print("***************************\n")

# -------------------------
# 5. Examples
# -------------------------
if __name__ == "__main__":
    run_agent("What are the key details of the remote work policy?")
    run_agent("What was the Q1 revenue?")
    run_agent("Tell me the profit value for Q2.")