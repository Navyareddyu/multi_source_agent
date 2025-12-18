# Add DeepSeek API Key to Vercel

## Quick Steps

1. **Go to Vercel Dashboard**: https://vercel.com/dashboard
2. **Click** on your project: `multi_source_agent-master`
3. **Go to**: Settings → Environment Variables
4. **Click**: "Add New"
5. **Fill in**:
   - **Key**: `DEEPSEEK_API_KEY`
   - **Value**: `sk-023f6ad5300c4d6197b8954cb2925edc`
   - **Environments**: Select all (Production, Preview, Development)
6. **Click**: "Save"
7. **Redeploy**: 
   - Go to Deployments tab
   - Click the three dots (⋯) on the latest deployment
   - Click "Redeploy"
   - Or wait for the next automatic deployment

## ✅ After Adding the Key

Once redeployed, your app will use DeepSeek AI to generate natural language responses instead of returning raw data.

## 🧪 Test It

After redeployment, try asking:
- "What was the Q1 revenue?"
- "Tell me about the remote work policy"
- "What is the company strategy?"

You should get AI-generated, human-like responses! 🎉

