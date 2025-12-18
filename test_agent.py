# test_agent.py - Simple test without LLM

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import sqlite3

# Test document search
def test_document_search():
    print("Testing document search...")
    try:
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
        docs = vectorstore.similarity_search("remote work policy", k=2)
        context = "\n---\n".join([d.page_content for d in docs])
        print(f"Document search result:\n{context}")
        return True
    except Exception as e:
        print(f"Document search error: {e}")
        return False

# Test SQL query
def test_sql_query():
    print("\nTesting SQL query...")
    try:
        conn = sqlite3.connect("agent_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM company_records WHERE metric='Revenue' AND quarter='Q1'")
        results = cursor.fetchall()
        conn.close()
        print(f"SQL query result: {results}")
        return True
    except Exception as e:
        print(f"SQL error: {e}")
        return False

if __name__ == "__main__":
    doc_ok = test_document_search()
    sql_ok = test_sql_query()
    
    if doc_ok and sql_ok:
        print("\n✅ Both tools working! Your agent should work fine.")
    else:
        print("\n❌ Some tools have issues. Check the errors above.")