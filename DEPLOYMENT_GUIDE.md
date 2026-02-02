# 🚀 Deployment Guide - SuperBryn Voice Agent

Complete guide to deploy both backend and frontend to production.

## 📋 Prerequisites

Before deploying, ensure you have:
- ✅ All API keys configured
- ✅ Supabase database set up
- ✅ LiveKit Cloud account (or self-hosted)
- ✅ GitHub account (for repos)

---

## 🔧 Part 1: Backend Deployment

The backend agent needs to run continuously. Recommended platforms:

### Option A: Railway (Recommended - Easiest)

1. **Sign up** at [railway.app](https://railway.app)

2. **Create new project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo" (or upload code)

3. **Configure environment variables**:
   ```env
   # LiveKit
   LIVEKIT_URL=wss://your-livekit-server.com
   LIVEKIT_API_KEY=your-api-key
   LIVEKIT_API_SECRET=your-api-secret
   
   # Speech Services
   DEEPGRAM_API_KEY=your-deepgram-key
   CARTESIA_API_KEY=your-cartesia-key
   
   # LLM (choose one)
   LLM_PROVIDER=openai
   LLM_MODEL=gpt-4o-mini
   OPENAI_API_KEY=your-key
   
   # Database
   SUPABASE_URL=your-supabase-url
   SUPABASE_KEY=your-supabase-key
   
   # Avatar (optional)
   AVATAR_PROVIDER=placeholder
   ENABLE_AVATAR_VIDEO=true
   ```

4. **Set build command**:
   - Build Command: (leave empty)
   - Start Command: `cd backend && python -m livekit.agents dev agent.py`

5. **Deploy**: Railway will automatically deploy and keep it running

### Option B: Render

1. **Sign up** at [render.com](https://render.com)

2. **Create new Web Service**:
   - Connect GitHub repo
   - Select backend directory

3. **Configure**:
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && python -m livekit.agents dev agent.py`
   - **Environment**: Python 3

4. **Add environment variables** (same as Railway above)

5. **Deploy**: Render will build and deploy

### Option C: Fly.io

1. **Install Fly CLI**: `curl -L https://fly.io/install.sh | sh`

2. **Login**: `fly auth login`

3. **Initialize** (in backend directory):
   ```bash
   cd backend
   fly launch
   ```

4. **Create `fly.toml`**:
   ```toml
   app = "your-app-name"
   primary_region = "iad"
   
   [build]
   
   [env]
     LIVEKIT_URL = "wss://your-livekit-server.com"
     # ... other env vars
   
   [[services]]
     internal_port = 8080
     protocol = "tcp"
   ```

5. **Deploy**: `fly deploy`

### Option D: Docker (Any Platform)

1. **Create `backend/Dockerfile`**:
   ```dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   COPY . .
   
   CMD ["python", "-m", "livekit.agents", "dev", "agent.py"]
   ```

2. **Deploy to any Docker platform** (Railway, Render, Fly.io, AWS, GCP, etc.)

---

## 🌐 Part 2: Frontend Deployment

### Option A: Vercel (Recommended)

1. **Sign up** at [vercel.com](https://vercel.com)

2. **Import project**:
   - Click "Add New Project"
   - Import from GitHub
   - Select your frontend repo

3. **Configure**:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

4. **Add environment variables**:
   ```env
   VITE_LIVEKIT_URL=wss://your-livekit-server.com
   VITE_AVATAR_PROVIDER=livekit-video
   ```

5. **Set up token API**:
   - Create `api/token.ts` in `frontend/api/` (already exists)
   - Vercel automatically handles serverless functions in `/api` folder

6. **Deploy**: Click "Deploy"

### Option B: Netlify

1. **Sign up** at [netlify.com](https://netlify.com)

2. **Import project**:
   - Click "Add new site" → "Import an existing project"
   - Connect GitHub repo

3. **Configure build**:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `frontend/dist`

4. **Add environment variables**:
   ```env
   VITE_LIVEKIT_URL=wss://your-livekit-server.com
   VITE_AVATAR_PROVIDER=livekit-video
   LIVEKIT_URL=wss://your-livekit-server.com
   LIVEKIT_API_KEY=your-api-key
   LIVEKIT_API_SECRET=your-api-secret
   ```

5. **Set up token function**:
   - Netlify Functions are in `netlify/functions/token.js` (already exists)
   - Netlify automatically detects and deploys functions

6. **Deploy**: Click "Deploy site"

### Option C: GitHub Pages (Static Only - No Serverless Functions)

**Note**: GitHub Pages doesn't support serverless functions. You'll need a separate token server.

1. **Build locally**:
   ```bash
   cd frontend
   npm run build
   ```

2. **Deploy to GitHub Pages**:
   - Go to repo Settings → Pages
   - Select `gh-pages` branch and `/dist` folder
   - Or use GitHub Actions

3. **Set up separate token server** (Railway, Render, etc.)

---

## 🔐 Part 3: Token Server Setup

The frontend needs a token server to generate LiveKit access tokens.

### For Vercel

Token API is automatically handled via `frontend/api/token.ts`:
- Vercel converts this to a serverless function
- Access at: `https://your-app.vercel.app/api/token`

### For Netlify

Token function is in `netlify/functions/token.js`:
- Netlify automatically deploys this
- Access at: `https://your-app.netlify.app/.netlify/functions/token`

### For Other Platforms

Create a separate token server:

**Option 1: Simple Express Server (Railway/Render)**

1. **Create `token-server/server.js`**:
   ```javascript
   const express = require('express');
   const { AccessToken } = require('livekit-server-sdk');
   
   const app = express();
   app.use(express.json());
   
   app.post('/api/token', (req, res) => {
     const { room, participant } = req.body;
     
     const token = new AccessToken(
       process.env.LIVEKIT_API_KEY,
       process.env.LIVEKIT_API_SECRET
     );
     
     token.identity = participant;
     token.addGrant({
       roomJoin: true,
       room: room,
       canPublish: true,
       canSubscribe: true,
     });
     
     res.json({ token: token.toJwt() });
   });
   
   app.listen(3000);
   ```

2. **Deploy to Railway/Render** with environment variables

**Option 2: Update Frontend to Use External Token Server**

Update `frontend/src/App.tsx`:
```typescript
const response = await fetch('https://your-token-server.com/api/token', {
  // ... same as before
});
```

---

## 📝 Part 4: Environment Variables Checklist

### Backend (.env)

```env
# LiveKit
LIVEKIT_URL=wss://your-livekit-server.com
LIVEKIT_API_KEY=your-api-key
LIVEKIT_API_SECRET=your-api-secret

# Speech Services
DEEPGRAM_API_KEY=your-deepgram-key
CARTESIA_API_KEY=your-cartesia-key

# LLM
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
OPENAI_API_KEY=your-key

# Database
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key

# Avatar (optional)
AVATAR_PROVIDER=placeholder
ENABLE_AVATAR_VIDEO=true
AVATAR_VIDEO_WIDTH=640
AVATAR_VIDEO_HEIGHT=360
AVATAR_VIDEO_FPS=15
```

### Frontend (.env)

```env
# LiveKit
VITE_LIVEKIT_URL=wss://your-livekit-server.com

# Avatar
VITE_AVATAR_PROVIDER=livekit-video

# Token Server (if separate)
VITE_TOKEN_SERVER_URL=https://your-token-server.com
```

### Token Server (.env) - If Separate

```env
LIVEKIT_URL=wss://your-livekit-server.com
LIVEKIT_API_KEY=your-api-key
LIVEKIT_API_SECRET=your-api-secret
```

---

## 🗄️ Part 5: Database Setup

1. **Create Supabase project**:
   - Go to [supabase.com](https://supabase.com)
   - Create new project
   - Wait for setup to complete

2. **Run migrations**:
   - Go to SQL Editor
   - Copy contents of `backend/supabase/migrations.sql`
   - Run the SQL

3. **Get credentials**:
   - Go to Project Settings → API
   - Copy `URL` and `anon` key
   - Add to backend environment variables

---

## ✅ Part 6: Post-Deployment Checklist

### Backend Verification

- [ ] Agent is running (check logs)
- [ ] No errors in startup logs
- [ ] Can see "registered_workers" in LiveKit dashboard
- [ ] Environment variables all set correctly

### Frontend Verification

- [ ] Site loads without errors
- [ ] Can click "Start Voice Call"
- [ ] Microphone permission requested
- [ ] Token API endpoint working (`/api/token` or `/.netlify/functions/token`)
- [ ] Can connect to LiveKit room

### End-to-End Testing

- [ ] Voice conversation works
- [ ] Avatar displays (if enabled)
- [ ] Tool calls work
- [ ] Tool calls display in UI
- [ ] Conversation summary generates
- [ ] Summary displays on frontend
- [ ] Database saves data correctly

---

## 🔍 Troubleshooting

### Backend Issues

**Agent not connecting:**
- Check `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`
- Verify agent is running (check logs)
- Check LiveKit dashboard for registered workers

**Database errors:**
- Verify `SUPABASE_URL` and `SUPABASE_KEY`
- Check migrations ran successfully
- Verify tables exist in Supabase dashboard

### Frontend Issues

**Token API not working:**
- Vercel: Check `api/token.ts` exists
- Netlify: Check `netlify/functions/token.js` exists
- Verify environment variables in deployment platform

**Can't connect to room:**
- Check `VITE_LIVEKIT_URL` is set
- Verify token API returns valid token
- Check browser console for errors

**Avatar not showing:**
- Check `VITE_AVATAR_PROVIDER` is set
- Verify backend is publishing video tracks
- Check browser console for video track errors

---

## 📚 Quick Deploy Commands

### Railway (Backend)
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize
cd backend
railway init

# Add environment variables
railway variables set LIVEKIT_URL=wss://...

# Deploy
railway up
```

### Vercel (Frontend)
```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
cd frontend
vercel

# Add environment variables
vercel env add VITE_LIVEKIT_URL
```

### Netlify (Frontend)
```bash
# Install Netlify CLI
npm i -g netlify-cli

# Login
netlify login

# Deploy
cd frontend
netlify deploy --prod

# Add environment variables via dashboard or:
netlify env:set VITE_LIVEKIT_URL wss://...
```

---

## 🎯 Recommended Deployment Setup

**For Best Results:**

1. **Backend**: Railway (easiest, good free tier)
2. **Frontend**: Vercel (best for React, automatic serverless functions)
3. **Database**: Supabase (already set up)

**Alternative:**
- **Backend**: Render
- **Frontend**: Netlify
- **Database**: Supabase

---

## 📞 Support

If you encounter issues:
1. Check deployment platform logs
2. Check browser console (frontend)
3. Check backend logs (agent)
4. Verify all environment variables are set
5. Test locally first before deploying

---

## 🎉 Success!

Once deployed, you'll have:
- ✅ Backend agent running 24/7
- ✅ Frontend accessible via URL
- ✅ Full voice agent functionality
- ✅ Database persistence
- ✅ Avatar display (if enabled)

**Your deployed link**: `https://your-frontend.vercel.app` (or netlify.app)
