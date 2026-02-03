# 🔧 Quick Fix: Token API 500 Error

## The Problem
You're seeing: `Token API returned 500: . Check that LIVEKIT_API_KEY, LIVEKIT_API_SECRET, and LIVEKIT_URL are set...`

This means the environment variables are **not set** in your Vercel deployment.

## The Solution (5 minutes)

### Step 1: Go to Vercel Dashboard
1. Go to [vercel.com](https://vercel.com)
2. Sign in to your account
3. Click on your project

### Step 2: Add Environment Variables
1. Click on **Settings** (in the top navigation)
2. Click on **Environment Variables** (in the left sidebar)
3. Click **Add New** button

### Step 3: Add Each Variable
Add these **three** variables one by one:

**Variable 1:**
- **Name**: `LIVEKIT_API_KEY`
- **Value**: Your LiveKit API key (from your LiveKit dashboard)
- **Environment**: Select **Production**, **Preview**, and **Development** (or at least Production)
- Click **Save**

**Variable 2:**
- **Name**: `LIVEKIT_API_SECRET`
- **Value**: Your LiveKit API secret (from your LiveKit dashboard)
- **Environment**: Select **Production**, **Preview**, and **Development** (or at least Production)
- Click **Save**

**Variable 3:**
- **Name**: `LIVEKIT_URL`
- **Value**: Your LiveKit server URL (e.g., `wss://your-project.livekit.cloud`)
- **Environment**: Select **Production**, **Preview**, and **Development** (or at least Production)
- Click **Save**

### Step 4: Redeploy
1. Go to **Deployments** tab
2. Click the **⋯** (three dots) on the latest deployment
3. Click **Redeploy**
4. Wait for deployment to complete (1-2 minutes)

### Step 5: Test
1. Visit your deployed site
2. Click "Start Voice Call"
3. The error should be gone! ✅

## Where to Find Your LiveKit Credentials

1. Go to [cloud.livekit.io](https://cloud.livekit.io) (or your LiveKit server)
2. Sign in to your account
3. Go to your project
4. Find:
   - **API Key**: Usually starts with `AP...`
   - **API Secret**: A long secret string
   - **Server URL**: Usually `wss://your-project.livekit.cloud`

## Still Not Working?

1. **Check the deployment logs**:
   - Go to Vercel → Your Project → Deployments
   - Click on the latest deployment
   - Check "Function Logs" for errors

2. **Verify the API file exists**:
   - Make sure `frontend/api/token.ts` exists in your codebase
   - Vercel automatically converts files in `api/` to serverless functions

3. **Test the endpoint directly**:
   ```bash
   curl -X POST https://your-project.vercel.app/api/token \
     -H "Content-Type: application/json" \
     -d '{"room":"test","participant":"test-user"}'
   ```
   
   Should return JSON with `token` and `url` fields.

4. **Double-check environment variables**:
   - Make sure they're set for the correct environment (Production/Preview)
   - Make sure there are no extra spaces in the values
   - Make sure the variable names are exactly: `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`, `LIVEKIT_URL`

## Common Mistakes

❌ **Setting variables only for Development** - Make sure to set them for Production too!
❌ **Typos in variable names** - Must be exactly: `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`, `LIVEKIT_URL`
❌ **Forgetting to redeploy** - You must redeploy after adding environment variables
❌ **Using wrong LiveKit URL format** - Should be `wss://...` not `https://...`
