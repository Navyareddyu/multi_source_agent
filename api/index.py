"""
Vercel serverless function - FastAPI app for multi-source agent
This is the main entry point for Vercel deployment
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import json

app = FastAPI(title="Multi-Source Agent API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# Embedded Data (for serverless demo)
# In production, replace with cloud services
# ============================================

# Embedded database records (normally from SQLite)
EMBEDDED_DB_DATA = [
    {"id": 1, "metric": "Revenue", "value": 150.5, "unit": "Million USD", "quarter": "Q1"},
    {"id": 2, "metric": "Profit", "value": 45.2, "unit": "Million USD", "quarter": "Q1"},
    {"id": 3, "metric": "Revenue", "value": 165.1, "unit": "Million USD", "quarter": "Q2"},
    {"id": 4, "metric": "Profit", "value": 52.8, "unit": "Million USD", "quarter": "Q2"},
    {"id": 5, "metric": "Total Employees", "value": 250, "unit": "People", "quarter": "Q1"},
]

# Embedded document data (normally from ChromaDB)
EMBEDDED_DOCUMENTS = {
    "remote work policy": """DOCUMENT TITLE: Remote Work Policy
The company supports a flexible remote work policy. All employees can work remotely up to two days per week, provided they have manager approval and maintain productivity. For full-time remote roles, a separate agreement is required.""",
    "company strategy": """DOCUMENT TITLE: Company Strategy
Our strategy focuses on three key pillars: innovation, customer satisfaction, and sustainable growth. We prioritize long-term value creation over short-term gains.""",
}

# ============================================
# Request/Response Models
# ============================================

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[ChatMessage]] = []

class ChatResponse(BaseModel):
    response: str
    tool_used: Optional[str] = None
    context: Optional[str] = None

# ============================================
# Core Functions (Serverless-compatible)
# ============================================

def run_sql_query(query: str) -> str:
    """Execute SQL-like queries on embedded data"""
    try:
        query_lower = query.lower()
        results = []
        
        # Simple query parsing for demo
        if "revenue" in query_lower:
            results = [r for r in EMBEDDED_DB_DATA if r["metric"] == "Revenue"]
        elif "profit" in query_lower:
            results = [r for r in EMBEDDED_DB_DATA if r["metric"] == "Profit"]
        elif "employees" in query_lower:
            results = [r for r in EMBEDDED_DB_DATA if r["metric"] == "Total Employees"]
        else:
            results = EMBEDDED_DB_DATA
        
        # Filter by quarter if specified
        if "q1" in query_lower:
            results = [r for r in results if r["quarter"] == "Q1"]
        elif "q2" in query_lower:
            results = [r for r in results if r["quarter"] == "Q2"]
        
        return f"Database Results: {json.dumps(results, indent=2)}"
    except Exception as e:
        return f"SQL Error: {e}"

def document_search(query: str) -> str:
    """Search embedded documents"""
    try:
        query_lower = query.lower()
        matches = []
        
        # Simple keyword matching
        for doc_key, doc_content in EMBEDDED_DOCUMENTS.items():
            if any(word in query_lower for word in doc_key.split()):
                matches.append(doc_content)
            elif any(word in doc_content.lower() for word in query_lower.split()):
                matches.append(doc_content)
        
        if not matches:
            # Default to remote work policy for policy-related queries
            if any(word in query_lower for word in ["policy", "remote", "work"]):
                matches.append(EMBEDDED_DOCUMENTS["remote work policy"])
            else:
                matches.append("\n---\n".join(EMBEDDED_DOCUMENTS.values()))
        
        return "Retrieved Context:\n" + "\n---\n".join(matches)
    except Exception as e:
        return f"Document search error: {e}"

def generate_response(question: str, context: str) -> str:
    """Generate response using context (LLM optional)"""
    # For demo: return formatted response
    # In production: integrate with OpenAI, Anthropic, etc.
    
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        try:
            import openai
            client = openai.OpenAI(api_key=openai_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. Answer the user's question based on the provided context. Be concise and accurate."},
                    {"role": "user", "content": f"Question: {question}\n\nContext: {context}\n\nAnswer:"}
                ],
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error using LLM: {e}. Here's the context: {context}"
    
    # Fallback: return context with formatting
    return f"""Based on the available information:

{context}

**Note**: For full LLM processing, set OPENAI_API_KEY environment variable in Vercel."""

# ============================================
# API Endpoints
# ============================================

@app.get("/")
async def root():
    return {
        "message": "Multi-Source Agent API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": ["/chat", "/health"]
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Handle chat requests - serverless compatible"""
    try:
        question = request.message
        question_lower = question.lower()
        
        tool_used = None
        context = ""
        
        # Determine which tool to use
        if any(word in question_lower for word in ['revenue', 'profit', 'q1', 'q2', 'employees', 'metric']):
            tool_used = "sql"
            # Generate SQL query based on question
            if 'revenue' in question_lower:
                if 'q1' in question_lower:
                    context = run_sql_query("SELECT * FROM company_records WHERE metric='Revenue' AND quarter='Q1'")
                elif 'q2' in question_lower:
                    context = run_sql_query("SELECT * FROM company_records WHERE metric='Revenue' AND quarter='Q2'")
                else:
                    context = run_sql_query("SELECT * FROM company_records WHERE metric='Revenue'")
            elif 'profit' in question_lower:
                if 'q1' in question_lower:
                    context = run_sql_query("SELECT * FROM company_records WHERE metric='Profit' AND quarter='Q1'")
                elif 'q2' in question_lower:
                    context = run_sql_query("SELECT * FROM company_records WHERE metric='Profit' AND quarter='Q2'")
                else:
                    context = run_sql_query("SELECT * FROM company_records WHERE metric='Profit'")
            elif 'employees' in question_lower:
                context = run_sql_query("SELECT * FROM company_records WHERE metric='Total Employees'")
            else:
                context = run_sql_query("SELECT * FROM company_records")
        
        elif any(word in question_lower for word in ['policy', 'remote', 'work', 'strategy', 'document']):
            tool_used = "document_search"
            context = document_search(question)
        
        else:
            # Search both sources
            tool_used = "both"
            doc_result = document_search(question)
            sql_result = run_sql_query("SELECT * FROM company_records LIMIT 3")
            context = f"{doc_result}\n\n{sql_result}"
        
        # Generate response
        response_text = generate_response(question, context)
        
        return ChatResponse(
            response=response_text,
            tool_used=tool_used,
            context=context[:200] + "..." if len(context) > 200 else context
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "multi-source-agent"}

# Vercel serverless function handler
# For Vercel, we need to export the app as 'app'
# Vercel will automatically wrap it with ASGI adapter

