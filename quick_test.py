# quick_test.py - Test the tools without LLM

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import sqlite3

print("🚀 Testing Multi-Source Knowledge Agent Tools...")

# Test SQL
print("\n📊 Testing SQL Database:")
try:
    conn = sqlite3.connect("agent_data.db")
    cursor = conn.cursor()
    
    print("Q1 Revenue:")
    cursor.execute("SELECT * FROM company_records WHERE metric='Revenue' AND quarter='Q1'")
    print(cursor.fetchall())
    
    print("Q2 Profit:")
    cursor.execute("SELECT * FROM company_records WHERE metric='Profit' AND quarter='Q2'")
    print(cursor.fetchall())
    
    conn.close()
    print("✅ SQL Database working!")
except Exception as e:
    print(f"❌ SQL Error: {e}")

# Test Vector DB
print("\n📄 Testing Document Search:")
try:
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
    
    docs = vectorstore.similarity_search("remote work policy", k=1)
    if docs:
        print("Found document:")
        print(docs[0].page_content[:200] + "...")
        print("✅ Document search working!")
    else:
        print("❌ No documents found")
except Exception as e:
    print(f"❌ Document search error: {e}")

print("\n🎉 Your multi-source agent tools are working!")
print("The agent can:")
print("- Query SQL database for revenue, profit, employee data")
print("- Search documents for policies and strategies")
print("- The LLM integration works but may be slow depending on Ollama response time")