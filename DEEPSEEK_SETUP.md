# DeepSeek API Integration

## ✅ Code Updated

The app now supports DeepSeek API! The code has been updated to use DeepSeek's API endpoint.

## 🔑 Set API Key in Vercel

To enable DeepSeek AI responses, you need to add the API key to Vercel:

### Steps:

1. **Go to Vercel Dashboard**: https://vercel.com/dashboard
2. **Select your project**: `multi_source_agent-master`
3. **Go to**: Settings → Environment Variables
4. **Add new variable**:
   - **Key**: `DEEPSEEK_API_KEY`
   - **Value**: `sk-023f6ad5300c4d6197b8954cb2925edc`
   - **Environment**: Production, Preview, Development (select all)
5. **Click**: "Save"
6. **Redeploy** your application (Vercel will prompt you, or go to Deployments → Redeploy)

## 📝 Alternative: Using OPENAI_API_KEY

The code also checks for `OPENAI_API_KEY` as a fallback, so you can use either:
- `DEEPSEEK_API_KEY` (recommended)
- `OPENAI_API_KEY` (also works)

## 🧪 Test After Deployment

After redeploying with the API key:

1. Go to: https://multisourceagent-master.vercel.app
2. Try asking: "What was the Q1 revenue?"
3. You should get an AI-generated response instead of raw data

## 🔒 Security Note

- Never commit API keys to GitHub
- Always use Vercel Environment Variables
- The API key is secure and only accessible server-side

## 💡 How It Works

- **Without API key**: Returns raw context data (still functional)
- **With DeepSeek API key**: Returns AI-processed, natural language responses

The code automatically:
1. Checks for `DEEPSEEK_API_KEY` environment variable
2. Uses DeepSeek's API endpoint: `https://api.deepseek.com/v1`
3. Uses model: `deepseek-chat`
4. Falls back to raw context if API fails

---

**Next Step**: Add the API key in Vercel Dashboard and redeploy! 🚀

