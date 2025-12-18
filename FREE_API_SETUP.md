# 🆓 Free API Key Setup Guide

## ✅ Free LLM API Options

I've updated the code to support **Groq API** which has a **generous free tier**!

### Option 1: Groq API (Recommended - Free & Fast) ⭐

**Why Groq?**
- ✅ **Completely FREE** (no credit card required for basic tier)
- ✅ **Very fast** responses (uses Groq's inference engine)
- ✅ **30 requests/minute** free tier
- ✅ OpenAI-compatible API (easy integration)

**How to Get Free Groq API Key:**

1. **Go to**: https://console.groq.com
2. **Sign up** for a free account (use email or Google/GitHub)
3. **Go to**: API Keys section
4. **Click**: "Create API Key"
5. **Copy** your API key (starts with `gsk_...`)
6. **Add to Vercel**:
   - Go to Vercel Dashboard → Your Project → Settings → Environment Variables
   - **Key**: `GROQ_API_KEY`
   - **Value**: Your Groq API key
   - **Environments**: Select all (Production, Preview, Development)
   - Click "Save"
7. **Redeploy** your app

**That's it!** Your app will now use free AI responses.

---

### Option 2: DeepSeek (If you have credits)

If your DeepSeek account has credits:
- Use `DEEPSEEK_API_KEY` (you already have this set up)

---

### Option 3: OpenAI (If you have credits)

If you have OpenAI credits:
- Use `OPENAI_API_KEY`

---

## 🔄 Priority Order

The app tries APIs in this order:
1. **Groq** (free) - `GROQ_API_KEY`
2. **DeepSeek** - `DEEPSEEK_API_KEY`
3. **OpenAI** - `OPENAI_API_KEY`
4. **Fallback** - Returns formatted data if none work

## 📝 Quick Setup Steps

1. **Get Groq API Key**: https://console.groq.com
2. **Add to Vercel**: Settings → Environment Variables
   - Key: `GROQ_API_KEY`
   - Value: Your Groq key
3. **Redeploy**: Go to Deployments → Redeploy

## ✅ After Setup

Once you add the Groq API key and redeploy:
- ✅ Fast AI responses
- ✅ No cost (free tier)
- ✅ Works immediately

---

**Get your free Groq API key here**: https://console.groq.com 🚀

