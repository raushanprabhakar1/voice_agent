# ⚡ Quick Deployment Guide

Fastest way to get your voice agent deployed.

## 🎯 Recommended Setup (15 minutes)

### Backend → Railway
### Frontend → Vercel

---

## 📦 Step 1: Deploy Backend (Railway)

### 1.1 Create Railway Account
- Go to [railway.app](https://railway.app)
- Sign up with GitHub

### 1.2 Create New Project
- Click "New Project"
- Select "Deploy from GitHub repo"
- Choose your backend repo (or create one)

### 1.3 Configure
- **Root Directory**: `backend`
- **Start Command**: `python -m livekit.agents dev agent.py`

### 1.4 Add Environment Variables
Click "Variables" tab and add:

```env
LIVEKIT_URL=wss://your-livekit-server.com
LIVEKIT_API_KEY=your-key
LIVEKIT_API_SECRET=your-secret
DEEPGRAM_API_KEY=your-key
CARTESIA_API_KEY=your-key
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
OPENAI_API_KEY=your-key
SUPABASE_URL=your-url
SUPABASE_KEY=your-key
AVATAR_PROVIDER=placeholder
ENABLE_AVATAR_VIDEO=true
```

### 1.5 Deploy
- Railway auto-deploys on push
- Or click "Deploy" button
- Check logs to verify agent started

**✅ Backend URL**: Railway provides a URL (not needed for frontend)

---

## 🌐 Step 2: Deploy Frontend (Vercel)

### 2.1 Create Vercel Account
- Go to [vercel.com](https://vercel.com)
- Sign up with GitHub

### 2.2 Import Project
- Click "Add New Project"
- Import from GitHub
- Select your frontend repo

### 2.3 Configure
- **Framework Preset**: Vite
- **Root Directory**: `frontend`
- **Build Command**: `npm run build`
- **Output Directory**: `dist`

### 2.4 Add Environment Variables
Click "Environment Variables" and add:

```env
VITE_LIVEKIT_URL=wss://your-livekit-server.com
VITE_AVATAR_PROVIDER=livekit-video
LIVEKIT_URL=wss://your-livekit-server.com
LIVEKIT_API_KEY=your-key
LIVEKIT_API_SECRET=your-secret
```

**Important**: 
- `VITE_*` variables are for frontend
- `LIVEKIT_*` variables are for the token API function

### 2.5 Deploy
- Click "Deploy"
- Wait for build to complete
- Your site is live!

**✅ Frontend URL**: `https://your-app.vercel.app`

---

## 🔍 Step 3: Verify Deployment

### Backend Check
1. Go to Railway dashboard
2. Check "Deployments" tab
3. Click on latest deployment
4. Check logs for:
   - ✅ "registered_workers" (agent connected)
   - ✅ No errors

### Frontend Check
1. Visit your Vercel URL
2. Click "Start Voice Call"
3. Grant microphone permission
4. Should connect to room
5. Agent should respond

### Test Flow
1. ✅ Voice conversation works
2. ✅ Avatar displays
3. ✅ Tool calls work
4. ✅ Summary generates

---

## 🐛 Common Issues

### Backend: Agent Not Connecting
- Check `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`
- Verify agent logs show "registered_workers"
- Check LiveKit dashboard

### Frontend: Token API Error
- Verify `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET` in Vercel env vars
- Check `api/token.ts` exists in frontend
- Test token endpoint: `https://your-app.vercel.app/api/token`

### Frontend: Can't Connect
- Check `VITE_LIVEKIT_URL` is set correctly
- Verify token API returns valid token
- Check browser console for errors

---

## 📝 Pre-Deployment Checklist

Before deploying, ensure:

- [ ] All API keys ready
- [ ] Supabase database set up
- [ ] Migrations run (`backend/supabase/migrations.sql`)
- [ ] Backend code tested locally
- [ ] Frontend code tested locally
- [ ] GitHub repos created (if using)

---

## 🚀 Alternative: Netlify (Frontend)

If you prefer Netlify:

1. **Sign up** at [netlify.com](https://netlify.com)
2. **Import project** from GitHub
3. **Configure**:
   - Base directory: `frontend`
   - Build command: `npm run build`
   - Publish directory: `frontend/dist`
4. **Add environment variables** (same as Vercel)
5. **Deploy**

Netlify automatically handles `netlify/functions/token.js` as a serverless function.

---

## 🎉 You're Done!

Once deployed:
- ✅ Backend running 24/7 on Railway
- ✅ Frontend live on Vercel/Netlify
- ✅ Full voice agent functionality
- ✅ Ready for users!

**Share your deployed link**: `https://your-app.vercel.app`

---

## 💡 Pro Tips

1. **Use Railway's free tier** for backend (500 hours/month)
2. **Use Vercel's free tier** for frontend (unlimited)
3. **Monitor logs** regularly
4. **Set up alerts** for errors
5. **Test thoroughly** before sharing

---

## 📚 Next Steps

- Add custom domain (optional)
- Set up monitoring
- Add analytics
- Optimize performance
- Scale as needed
