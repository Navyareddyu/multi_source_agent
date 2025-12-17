# working_agent.py - Simple Multi-Source Knowledge Agent

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from langchain_community.chat_models import ChatOllama
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
import sqlite3

# Initialize embeddings and vectorstore once
print("Loading embeddings and vector database...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
print("✅ Vector database loaded!")

# Initialize LLM
llm = ChatOllama(model="mistral", base_url="http://localhost:11434", temperature=0.0)

def document_search(query: str) -> str:
    """Search through company documents and policies for information."""
    try:
        docs = vectorstore.similarity_search(query, k=2)
        context = "\n---\n".join([d.page_content for d in docs])
        return f"Retrieved Context:\n{context}"
    except Exception as e:
        return f"Document search error: {e}"

def run_sql_query(query: str) -> str:
    """Execute SQL queries on the company database."""
    try:
        conn = sqlite3.connect("agent_data.db")
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return f"Results: {results}"
    except Exception as e:
        return f"SQL Error: {e}"

def run_agent(question: str):
    print(f"\n🤖 USER: {question}")
    
    question_lower = question.lower()
    context = ""
    
    # Determine which tool to use
    if any(word in question_lower for word in ['revenue', 'profit', 'q1', 'q2', 'employees', 'metric']):
        print("📊 Using SQL database...")
        if 'revenue' in question_lower and 'q1' in question_lower:
            context = run_sql_query("SELECT * FROM company_records WHERE metric='Revenue' AND quarter='Q1'")
        elif 'revenue' in question_lower and 'q2' in question_lower:
            context = run_sql_query("SELECT * FROM company_records WHERE metric='Revenue' AND quarter='Q2'")
        elif 'profit' in question_lower and 'q1' in question_lower:
            context = run_sql_query("SELECT * FROM company_records WHERE metric='Profit' AND quarter='Q1'")
        elif 'profit' in question_lower and 'q2' in question_lower:
            context = run_sql_query("SELECT * FROM company_records WHERE metric='Profit' AND quarter='Q2'")
        elif 'revenue' in question_lower:
            context = run_sql_query("SELECT * FROM company_records WHERE metric='Revenue'")
        elif 'profit' in question_lower:
            context = run_sql_query("SELECT * FROM company_records WHERE metric='Profit'")
        else:
            context = run_sql_query("SELECT * FROM company_records")
    
    elif any(word in question_lower for word in ['policy', 'remote', 'work', 'strategy', 'phoenix']):
        print("📄 Using document search...")
        context = document_search(question)
    
    else:
        print("🔍 Searching both sources...")
        doc_result = document_search(question)
        sql_result = run_sql_query("SELECT * FROM company_records LIMIT 3")
        context = f"{doc_result}\n\n{sql_result}"
    
    # Create prompt and get LLM response
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Answer based on the provided context. Be concise."),
        ("human", f"Question: {question}\n\nContext: {context}\n\nAnswer:")
    ])
    
    try:
        chain = prompt | llm
        response = chain.invoke({})
        print(f"\n💡 AGENT ANSWER:\n{response.content}")
    except Exception as e:
        print(f"\n❌ LLM Error: {e}")
        print(f"📋 Raw context: {context}")
    
    print("=" * 50)

if __name__ == "__main__":
    print("🚀 Starting Multi-Source Knowledge Agent...")
    
    # Test questions
    run_agent("What are the key details of the remote work policy?")
    run_agent("What was the Q1 revenue?")
    run_agent("Tell me the profit value for Q2.")