# Vercel Environment Variables Setup

## Issue

Getting 500 error: "LiveKit configuration missing"

This means the token API is working, but the environment variables are not set in Vercel.

## Solution: Add Environment Variables

### Step 1: Go to Vercel Dashboard

1. Go to [vercel.com](https://vercel.com)
2. Sign in to your account
3. Click on your project

### Step 2: Navigate to Environment Variables

1. Click on **"Settings"** tab (top navigation)
2. Click on **"Environment Variables"** in the left sidebar

### Step 3: Add Required Variables

Click **"Add New"** and add these **three** variables:

#### Variable 1: LIVEKIT_URL
- **Key**: `LIVEKIT_URL`
- **Value**: `wss://your-livekit-server.com` (your actual LiveKit server URL)
- **Environment**: Select **Production**, **Preview**, and **Development** (or at least **Production**)

#### Variable 2: LIVEKIT_API_KEY
- **Key**: `LIVEKIT_API_KEY`
- **Value**: Your LiveKit API key (starts with `AP...`)
- **Environment**: Select **Production**, **Preview**, and **Development** (or at least **Production**)

#### Variable 3: LIVEKIT_API_SECRET
- **Key**: `LIVEKIT_API_SECRET`
- **Value**: Your LiveKit API secret (long string)
- **Environment**: Select **Production**, **Preview**, and **Development** (or at least **Production**)

### Step 4: Save and Redeploy

1. Click **"Save"** after adding each variable
2. After adding all three, go to **"Deployments"** tab
3. Click the **"..."** menu on the latest deployment
4. Click **"Redeploy"**
5. Select **"Use existing Build Cache"** or **"Redeploy"** (either works)
6. Wait for deployment to complete

### Step 5: Verify

After redeploying, test the endpoint:
```bash
curl -X POST https://your-app.vercel.app/api/token \
  -H "Content-Type: application/json" \
  -d '{"room":"test","participant":"test-user"}'
```

**Expected Response** (200 OK):
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "url": "wss://your-livekit-server.com"
}
```

**If you still get 500**: Check that all three variables are set correctly

## Where to Get LiveKit Credentials

### If Using LiveKit Cloud

1. Go to [cloud.livekit.io](https://cloud.livekit.io)
2. Sign in to your account
3. Go to your project
4. Go to **Settings** → **Keys**
5. Copy:
   - **Server URL**: `wss://your-project.livekit.cloud`
   - **API Key**: `AP...`
   - **API Secret**: (long string)

### If Using Self-Hosted LiveKit

1. Check your LiveKit server configuration
2. Get the WebSocket URL (usually `wss://your-domain.com`)
3. Get API key and secret from your LiveKit config

## Important Notes

1. **All Three Environments**: Make sure to add variables for **Production**, **Preview**, and **Development** environments
   - Or at minimum, add them for **Production**

2. **Case Sensitive**: Variable names are case-sensitive:
   - ✅ `LIVEKIT_URL` (correct)
   - ❌ `livekit_url` (wrong)
   - ❌ `LiveKit_URL` (wrong)

3. **No Spaces**: Make sure there are no extra spaces in the values

4. **Redeploy Required**: After adding environment variables, you **must redeploy** for them to take effect

## Quick Checklist

- [ ] `LIVEKIT_URL` is set (starts with `wss://`)
- [ ] `LIVEKIT_API_KEY` is set (starts with `AP...`)
- [ ] `LIVEKIT_API_SECRET` is set (long string)
- [ ] All three are set for **Production** environment (at minimum)
- [ ] Redeployed after adding variables
- [ ] Test endpoint returns 200 (not 500)

## Troubleshooting

### Still Getting 500 After Adding Variables

1. **Check variable names**: Make sure they're exactly:
   - `LIVEKIT_URL`
   - `LIVEKIT_API_KEY`
   - `LIVEKIT_API_SECRET`

2. **Check values**: 
   - `LIVEKIT_URL` should start with `wss://`
   - `LIVEKIT_API_KEY` should start with `AP...`
   - `LIVEKIT_API_SECRET` should be a long string

3. **Redeploy**: Make sure you redeployed after adding variables

4. **Check deployment logs**: 
   - Go to Deployments → Latest deployment → Function Logs
   - Look for errors related to environment variables

### Getting "LiveKit configuration missing"

This means one or more of the three variables are not set. Double-check:
- All three variables are added
- Variable names are correct (case-sensitive)
- Values are correct
- Variables are set for the correct environment (Production)

### Variables Not Available in Function

If variables are set but function still can't access them:
1. Make sure you redeployed after adding variables
2. Check that variables are set for the correct environment
3. Try removing and re-adding the variables
4. Check Vercel function logs for specific errors
