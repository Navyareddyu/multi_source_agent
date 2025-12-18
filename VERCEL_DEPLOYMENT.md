# Vercel Deployment Guide

## ✅ What's Been Set Up

Your app has been converted to work on Vercel's serverless platform:

1. **FastAPI Backend** (`api/index.py`)
   - Serverless-compatible functions
   - Embedded data for demo (can be replaced with cloud services)
   - Supports OpenAI API integration (optional)

2. **Frontend** (`public/index.html`)
   - Modern, responsive chat interface
   - Replaces Streamlit UI
   - Works with the FastAPI backend

3. **Vercel Configuration** (`vercel.json`)
   - Routes API calls to serverless functions
   - Serves static files from `/public`
   - Python 3.9 runtime

## 🚀 Deploy to Vercel

### Option 1: Deploy via Vercel CLI (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel

# Follow prompts:
# - Set up and deploy? Yes
# - Which scope? (your account)
# - Link to existing project? No
# - Project name? multi-source-agent (or your choice)
# - Directory? ./
```

### Option 2: Deploy via GitHub

1. **Push to GitHub** (already done ✅)
2. **Go to vercel.com**
3. **Import your repository**: `Navyareddyu/multi_source_agent`
4. **Configure:**
   - Framework Preset: Other
   - Root Directory: ./
   - Build Command: (leave empty)
   - Output Directory: (leave empty)
5. **Click Deploy**

## ⚙️ Optional: Add OpenAI API (For Better Responses)

To enable full LLM processing:

1. **Get OpenAI API Key** from https://platform.openai.com/api-keys
2. **In Vercel Dashboard:**
   - Go to your project → Settings → Environment Variables
   - Add: `OPENAI_API_KEY` = `your-api-key-here`
   - Redeploy

Without OpenAI, the app will return the context data directly (still functional, just without LLM processing).

## 📁 Project Structure

```
multi_source_agent/
├── api/
│   ├── index.py          # FastAPI serverless function
│   └── requirements.txt  # Python dependencies
├── public/
│   └── index.html        # Frontend UI
├── vercel.json           # Vercel configuration
└── .vercelignore         # Files to exclude
```

## 🔍 How It Works

### Serverless Architecture

1. **Frontend** (`/`) → Served as static HTML from `/public`
2. **API** (`/api/chat`) → FastAPI function on Vercel serverless
3. **Data** → Currently embedded (can be replaced with cloud DB)

### Request Flow

```
User types message
  ↓
Frontend sends POST to /api/chat
  ↓
Vercel invokes serverless function (api/index.py)
  ↓
Function processes query (SQL/document search)
  ↓
Returns response to frontend
  ↓
UI displays result
```

## 🔄 Updating Data

### Current: Embedded Data
The app uses embedded data in `api/index.py`:
- `EMBEDDED_DB_DATA` - Database records
- `EMBEDDED_DOCUMENTS` - Policy documents

### Future: Cloud Services

To use cloud services, update `api/index.py`:

**For Database:**
```python
# Replace run_sql_query() with:
import psycopg2  # or your DB client
def run_sql_query(query: str) -> str:
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    # ... execute query
```

**For Vector DB:**
```python
# Replace document_search() with:
import pinecone  # or chromadb cloud
def document_search(query: str) -> str:
    # ... cloud vector search
```

## 🧪 Testing Locally

```bash
# Install dependencies
pip install -r api/requirements.txt

# Run FastAPI locally
cd api
uvicorn index:app --reload

# Open browser to http://localhost:8000
# Or serve the HTML file separately
```

## 📊 What Works Now

✅ **SQL Queries**: Revenue, profit, Q1, Q2 data  
✅ **Document Search**: Remote work policy, company strategy  
✅ **Chat Interface**: Modern UI with message history  
✅ **Serverless Ready**: Works on Vercel platform  
✅ **Optional LLM**: Can integrate OpenAI for better responses  

## 🐛 Troubleshooting

**Issue: "Module not found"**
- Check `api/requirements.txt` includes all dependencies
- Redeploy after updating requirements

**Issue: "Function timeout"**
- Increase `maxDuration` in `vercel.json` (max 60s on Pro plan)

**Issue: "CORS error"**
- Already handled in `api/index.py` with CORS middleware

**Issue: "404 on /api/chat"**
- Check `vercel.json` routes are correct
- Ensure `api/index.py` exists

## 📝 Next Steps

1. Deploy to Vercel (see above)
2. Test the deployed app
3. (Optional) Add OpenAI API key for LLM processing
4. (Optional) Replace embedded data with cloud services

Your app is now ready for Vercel! 🎉

