# 🚀 Step-by-Step Deployment Guide

Follow these steps to deploy your voice agent to production.

## 📋 Pre-Deployment Checklist

Before starting, make sure you have:

- [ ] All API keys ready (LiveKit, Deepgram, Cartesia, LLM, Supabase)
- [ ] Supabase database set up and migrations run
- [ ] GitHub account (for connecting repos)
- [ ] Code tested locally and working

---

## 🎯 Recommended Setup

**Backend**: Railway (easiest, good free tier)  
**Frontend**: Vercel (best for React, automatic serverless functions)

---

## Part 1: Deploy Backend to Railway

### Step 1.1: Create Railway Account

1. Go to [railway.app](https://railway.app)
2. Click "Start a New Project"
3. Sign up with GitHub (recommended)

### Step 1.2: Create New Project

1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. If your code is not on GitHub yet:
   - Create a new GitHub repository
   - Push your code to GitHub
   - Then select it in Railway

### Step 1.3: Configure Project

1. **Set Root Directory**:
   - In Railway project settings, go to "Settings"
   - Under "Source", set "Root Directory" to: `backend`

2. **Set Start Command**:
   - Go to "Settings" → "Deploy"
   - Set "Start Command" to:
     ```
     python agent.py
     ```

3. **Set Build Command** (leave empty or set to):
   ```
   pip install -r requirements.txt
   ```

### Step 1.4: Add Environment Variables

1. Go to "Variables" tab in Railway
2. Click "New Variable" and add each of these:

```env
# LiveKit (REQUIRED)
LIVEKIT_URL=wss://your-livekit-server.com
LIVEKIT_API_KEY=your-api-key
LIVEKIT_API_SECRET=your-api-secret

# Speech Services (REQUIRED)
DEEPGRAM_API_KEY=your-deepgram-key
CARTESIA_API_KEY=your-cartesia-key

# LLM (REQUIRED - choose one provider)
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
OPENAI_API_KEY=your-openai-key

# OR for Azure OpenAI:
# LLM_PROVIDER=azure
# AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
# AZURE_OPENAI_API_KEY=your-azure-key
# AZURE_OPENAI_API_VERSION=2024-02-15-preview
# AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini

# OR for OpenRouter:
# LLM_PROVIDER=openrouter
# LLM_MODEL=google/gemini-flash-1.5
# OPENROUTER_API_KEY=sk-or-v1-your-key

# Database (REQUIRED)
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key

# Avatar (OPTIONAL)
AVATAR_PROVIDER=placeholder
ENABLE_AVATAR_VIDEO=true
AVATAR_VIDEO_WIDTH=640
AVATAR_VIDEO_HEIGHT=360
AVATAR_VIDEO_FPS=15
```

**Important**: Replace all `your-*` values with your actual API keys!

### Step 1.5: Deploy

1. Railway will automatically deploy when you push to GitHub
2. Or click "Deploy" button manually
3. Go to "Deployments" tab to see build progress
4. Check "Logs" tab to verify agent started successfully

### Step 1.6: Verify Backend

Look for these in the logs:
- ✅ "registered_workers" (agent connected to LiveKit)
- ✅ No errors
- ✅ Agent is listening for jobs

**✅ Backend is deployed!** Railway will keep it running 24/7.

---

## Part 2: Deploy Frontend to Vercel

### Step 2.1: Create Vercel Account

1. Go to [vercel.com](https://vercel.com)
2. Click "Sign Up"
3. Sign up with GitHub (recommended)

### Step 2.2: Import Project

1. Click "Add New Project"
2. Click "Import Git Repository"
3. Select your GitHub repository
4. Click "Import"

### Step 2.3: Configure Project

**Note**: Vercel's UI may vary. If you don't see these options during import, you can set them after importing in Settings.

**During Import:**
1. **Framework Preset**: 
   - Look for dropdown labeled "Framework Preset" or "Framework"
   - Select **"Vite"** (or "Other" if Vite not listed - it will auto-detect)
2. **Root Directory**: 
   - Look for "Root Directory" field
   - Set to: `frontend`
   - Or click folder icon to browse and select `frontend` folder
3. **Build Command**: Should auto-fill as `npm run build` (if not, set manually)
4. **Output Directory**: Should auto-fill as `dist` (if not, set manually)
5. **Install Command**: Should auto-fill as `npm install` (if not, set manually)

**If you can't find these during import:**
1. Import the project with default settings
2. After import, go to **Settings** → **General**
3. Set **Root Directory** to: `frontend`
4. Go to **Settings** → **Build & Development Settings**
5. Set Framework to "Vite", Build Command to `npm run build`, Output Directory to `dist`

**Alternative**: If Root Directory setting is not available, use these build commands:
- **Build Command**: `cd frontend && npm run build`
- **Output Directory**: `frontend/dist`
- **Install Command**: `cd frontend && npm install`

### Step 2.4: Add Environment Variables

1. Before deploying, click "Environment Variables"
2. Add these variables:

```env
# Frontend variables (VITE_ prefix)
VITE_LIVEKIT_URL=wss://your-livekit-server.com
VITE_AVATAR_PROVIDER=livekit-video

# Token API variables (for serverless function)
LIVEKIT_URL=wss://your-livekit-server.com
LIVEKIT_API_KEY=your-api-key
LIVEKIT_API_SECRET=your-api-secret
```

**Important**: 
- `VITE_*` variables are exposed to the frontend
- `LIVEKIT_*` variables are for the serverless function only

### Step 2.5: Deploy

1. Click "Deploy" button
2. Wait for build to complete (usually 1-2 minutes)
3. Your site will be live at: `https://your-project-name.vercel.app`

### Step 2.6: Verify Frontend

1. Visit your Vercel URL
2. Open browser console (F12)
3. Click "Start Voice Call"
4. Should see:
   - ✅ Microphone permission requested
   - ✅ Connection to LiveKit
   - ✅ Agent responds

**✅ Frontend is deployed!**

---

## Part 3: Verify Token API

The token API should work automatically with Vercel.

### Test Token API

1. Visit: `https://your-project.vercel.app/api/token`
2. Should see an error (that's OK - it needs POST request)
3. Or test with curl:

```bash
curl -X POST https://your-project.vercel.app/api/token \
  -H "Content-Type: application/json" \
  -d '{"room":"test-room","participant":"test-user"}'
```

Should return a JSON with `token` and `url`.

**✅ Token API is working!**

---

## Part 4: End-to-End Testing

### Test Complete Flow

1. **Open your deployed frontend**: `https://your-project.vercel.app`

2. **Start a call**:
   - Click "Start Voice Call"
   - Grant microphone permission
   - Wait for connection

3. **Test conversation**:
   - Say: "Hi, I want to book an appointment"
   - Agent should respond
   - Say your phone number when asked
   - Ask to book an appointment
   - Verify tool calls appear in UI
   - End conversation
   - Verify summary appears

4. **Check backend logs** (Railway):
   - Go to Railway dashboard
   - Check "Logs" tab
   - Should see conversation logs
   - Should see tool calls being executed

5. **Check database** (Supabase):
   - Go to Supabase dashboard
   - Check `appointments` table
   - Check `conversation_summaries` table
   - Should see your test data

**✅ Everything is working!**

---

## 🐛 Troubleshooting

### Backend: Agent Not Connecting

**Symptoms**: No "registered_workers" in logs

**Fix**:
1. Check `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET` in Railway
2. Verify values are correct (no extra spaces)
3. Check LiveKit dashboard to see if agent appears
4. Restart deployment in Railway

### Frontend: Token API Error

**Symptoms**: "Failed to get access token" error

**Fix**:
1. Check `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET` in Vercel env vars
2. Verify `api/token.ts` exists in `frontend/api/` folder
3. Check Vercel function logs
4. Test token endpoint directly

### Frontend: Can't Connect to Room

**Symptoms**: Connection fails, no agent response

**Fix**:
1. Check `VITE_LIVEKIT_URL` is set correctly in Vercel
2. Verify token API returns valid token
3. Check browser console for errors
4. Verify backend agent is running (Railway logs)

### Avatar Not Showing

**Symptoms**: Placeholder or no video

**Fix**:
1. Check `VITE_AVATAR_PROVIDER` is set
2. Verify `ENABLE_AVATAR_VIDEO=true` in backend
3. Check backend logs for video track publishing
4. Check browser console for video errors

### Tool Calls Not Showing

**Symptoms**: Tool calls work but don't appear in UI

**Fix**:
1. Check browser console for data channel errors
2. Verify backend is sending tool call data
3. Check `ToolCallDisplay` component is rendering
4. Check data channel is connected

---

## 📝 Environment Variables Reference

### Backend (Railway)

```env
# Required
LIVEKIT_URL=wss://...
LIVEKIT_API_KEY=...
LIVEKIT_API_SECRET=...
DEEPGRAM_API_KEY=...
CARTESIA_API_KEY=...
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
OPENAI_API_KEY=...
SUPABASE_URL=...
SUPABASE_KEY=...

# Optional
AVATAR_PROVIDER=placeholder
ENABLE_AVATAR_VIDEO=true
```

### Frontend (Vercel)

```env
# Required (for frontend)
VITE_LIVEKIT_URL=wss://...

# Required (for token API)
LIVEKIT_URL=wss://...
LIVEKIT_API_KEY=...
LIVEKIT_API_SECRET=...

# Optional
VITE_AVATAR_PROVIDER=livekit-video
```

---

## 🎉 Success!

Once deployed, you have:

- ✅ Backend agent running 24/7 on Railway
- ✅ Frontend live on Vercel
- ✅ Token API working automatically
- ✅ Full voice agent functionality
- ✅ Database persistence
- ✅ Tool call visualization
- ✅ Conversation summaries

**Your deployed link**: `https://your-project.vercel.app`

---

## 🔄 Updating Deployment

### Update Backend

1. Make changes to code
2. Push to GitHub
3. Railway auto-deploys (or click "Redeploy")

### Update Frontend

1. Make changes to code
2. Push to GitHub
3. Vercel auto-deploys (or click "Redeploy")

---

## 💡 Pro Tips

1. **Monitor logs regularly**: Check Railway and Vercel logs for errors
2. **Set up alerts**: Configure email alerts for deployment failures
3. **Use custom domain**: Add your own domain in Vercel settings
4. **Test before sharing**: Always test thoroughly before sharing link
5. **Keep API keys secure**: Never commit `.env` files to GitHub

---

## 📚 Additional Resources

- [Railway Docs](https://docs.railway.app/)
- [Vercel Docs](https://vercel.com/docs)
- [LiveKit Docs](https://docs.livekit.io/)
- [Full Deployment Guide](./DEPLOYMENT_GUIDE.md)
- [Quick Deploy Guide](./QUICK_DEPLOY.md)

---

## 🆘 Need Help?

If you encounter issues:

1. Check the troubleshooting section above
2. Review deployment platform logs
3. Check browser console for frontend errors
4. Verify all environment variables are set correctly
5. Test locally first to isolate issues

Good luck with your deployment! 🚀
