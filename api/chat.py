"""
Vercel serverless function for /api/chat
Each file in api/ becomes a serverless function at that path
"""

from http.server import BaseHTTPRequestHandler
import json
import os

# Embedded Data
EMBEDDED_DB_DATA = [
    {"id": 1, "metric": "Revenue", "value": 150.5, "unit": "Million USD", "quarter": "Q1"},
    {"id": 2, "metric": "Profit", "value": 45.2, "unit": "Million USD", "quarter": "Q1"},
    {"id": 3, "metric": "Revenue", "value": 165.1, "unit": "Million USD", "quarter": "Q2"},
    {"id": 4, "metric": "Profit", "value": 52.8, "unit": "Million USD", "quarter": "Q2"},
    {"id": 5, "metric": "Total Employees", "value": 250, "unit": "People", "quarter": "Q1"},
]

EMBEDDED_DOCUMENTS = {
    "remote work policy": """DOCUMENT TITLE: Remote Work Policy
The company supports a flexible remote work policy. All employees can work remotely up to two days per week, provided they have manager approval and maintain productivity. For full-time remote roles, a separate agreement is required.""",
    "company strategy": """DOCUMENT TITLE: Company Strategy
Our strategy focuses on three key pillars: innovation, customer satisfaction, and sustainable growth. We prioritize long-term value creation over short-term gains.""",
}

def run_sql_query(query: str) -> str:
    try:
        query_lower = query.lower()
        results = []
        
        if "revenue" in query_lower:
            results = [r for r in EMBEDDED_DB_DATA if r["metric"] == "Revenue"]
        elif "profit" in query_lower:
            results = [r for r in EMBEDDED_DB_DATA if r["metric"] == "Profit"]
        elif "employees" in query_lower:
            results = [r for r in EMBEDDED_DB_DATA if r["metric"] == "Total Employees"]
        else:
            results = EMBEDDED_DB_DATA
        
        if "q1" in query_lower:
            results = [r for r in results if r["quarter"] == "Q1"]
        elif "q2" in query_lower:
            results = [r for r in results if r["quarter"] == "Q2"]
        
        return f"Database Results: {json.dumps(results, indent=2)}"
    except Exception as e:
        return f"SQL Error: {e}"

def document_search(query: str) -> str:
    try:
        query_lower = query.lower()
        matches = []
        
        for doc_key, doc_content in EMBEDDED_DOCUMENTS.items():
            if any(word in query_lower for word in doc_key.split()):
                matches.append(doc_content)
            elif any(word in doc_content.lower() for word in query_lower.split()):
                matches.append(doc_content)
        
        if not matches:
            if any(word in query_lower for word in ["policy", "remote", "work"]):
                matches.append(EMBEDDED_DOCUMENTS["remote work policy"])
            else:
                matches.append("\n---\n".join(EMBEDDED_DOCUMENTS.values()))
        
        return "Retrieved Context:\n" + "\n---\n".join(matches)
    except Exception as e:
        return f"Document search error: {e}"

def generate_response(question: str, context: str) -> str:
    # Try DeepSeek API first, then fall back to OpenAI format
    deepseek_key = os.getenv("DEEPSEEK_API_KEY") or os.getenv("OPENAI_API_KEY")
    
    if deepseek_key:
        try:
            import openai
            # DeepSeek uses OpenAI-compatible API but different endpoint
            client = openai.OpenAI(
                api_key=deepseek_key,
                base_url="https://api.deepseek.com/v1"
            )
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. Answer the user's question based on the provided context. Be concise and accurate."},
                    {"role": "user", "content": f"Question: {question}\n\nContext: {context}\n\nAnswer:"}
                ],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            # Return formatted context data if LLM fails (better than error message)
            error_msg = str(e)
            if "Insufficient Balance" in error_msg or "402" in error_msg:
                return f"""Based on the available information:

{context}

*Note: AI processing is currently unavailable due to insufficient API balance. The data above contains all the relevant information.*"""
            else:
                return f"""Based on the available information:

{context}

*Note: AI processing encountered an error. The data above contains all the relevant information.*"""
    
    # No API key - return formatted context
    return f"""Based on the available information:

{context}

**Note**: For AI-processed responses, add DEEPSEEK_API_KEY or OPENAI_API_KEY in Vercel environment variables."""

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            question = data.get('message', '')
            question_lower = question.lower()
            
            tool_used = None
            context = ""
            
            if any(word in question_lower for word in ['revenue', 'profit', 'q1', 'q2', 'employees', 'metric']):
                tool_used = "sql"
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
                tool_used = "both"
                doc_result = document_search(question)
                sql_result = run_sql_query("SELECT * FROM company_records LIMIT 3")
                context = f"{doc_result}\n\n{sql_result}"
            
            response_text = generate_response(question, context)
            
            response = {
                "response": response_text,
                "tool_used": tool_used,
                "context": context[:200] + "..." if len(context) > 200 else context
            }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
