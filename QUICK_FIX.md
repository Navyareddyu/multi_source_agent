# Quick Fix Guide

## The Problem
```
Vercel → NOT_FOUND Error → Your Streamlit app
```

## Why It Happens
- Streamlit needs a **persistent server** (runs all day)
- Vercel provides **serverless functions** (appear/disappear per request)
- They're incompatible!

## The Fix (Choose One)

### Option 1: Streamlit Cloud ⭐ EASIEST
```bash
# 1. Push to GitHub
git add .
git commit -m "Ready for deployment"
git push

# 2. Go to share.streamlit.io
# 3. Connect repo → Deploy
# Done!
```

### Option 2: Railway/Render
```bash
# 1. Create account on railway.app or render.com
# 2. Connect GitHub repo
# 3. Set start command: streamlit run app.py
# 4. Deploy
```

### Option 3: Convert to FastAPI (for Vercel)
```bash
# See api/agent.py for example
# Requires rewriting UI (React/HTML instead of Streamlit)
```

## What Needs to Change for Cloud

### ❌ Current (Local Only)
```python
llm = ChatOllama(model="mistral")  # localhost:11434
conn = sqlite3.connect("agent_data.db")  # Local file
vectorstore = Chroma(persist_directory="./chroma_db")  # Local files
```

### ✅ Cloud-Ready
```python
# Use cloud LLM service
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Use cloud database
import psycopg2
conn = psycopg2.connect(os.getenv("DATABASE_URL"))

# Use cloud vector DB
import pinecone
pinecone.init(api_key=os.getenv("PINECONE_API_KEY"))
```

## Checklist

- [ ] Choose deployment platform
- [ ] Update LLM connection (remove localhost)
- [ ] Update database connection (use cloud DB)
- [ ] Update vector store (use cloud service)
- [ ] Test locally first
- [ ] Deploy!

## Need Help?

- **DEPLOYMENT_GUIDE.md** - Full explanation
- **WHY_NOT_VERCEL.md** - Technical deep dive
- **SOLUTION_SUMMARY.md** - Overview

