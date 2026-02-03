# Token API Troubleshooting Guide

## Error: "Failed to get access token"

This error occurs when the frontend cannot get a LiveKit access token from the token API endpoint.

## Common Causes & Solutions

### 1. Environment Variables Not Set

**Symptom**: Token API returns 500 error with "LiveKit configuration missing"

**Solution**:
- Go to your deployment platform (Vercel/Netlify)
- Navigate to **Settings** → **Environment Variables**
- Add these variables:
  ```env
  LIVEKIT_URL=wss://your-livekit-server.com
  LIVEKIT_API_KEY=your-api-key
  LIVEKIT_API_SECRET=your-api-secret
  ```
- **Important**: Make sure to add them for **Production**, **Preview**, and **Development** environments
- **Redeploy** after adding variables

### 2. Token API Endpoint Not Found (404)

**Symptom**: Token API returns 404 error

**For Vercel**:
- Make sure `frontend/api/token.ts` exists
- The file should be in the `api/` folder at the root of your frontend directory
- Vercel automatically converts files in `api/` to serverless functions
- Check Vercel deployment logs to see if the function was built

**For Netlify**:
- Make sure `frontend/netlify/functions/token.js` exists
- Netlify automatically detects functions in `netlify/functions/`
- Check Netlify deployment logs

**Solution**:
1. Verify the file exists in the correct location
2. Check deployment logs for build errors
3. Redeploy if needed

### 3. CORS Issues

**Symptom**: Network error or CORS error in browser console

**Solution**:
- Token API should handle CORS automatically
- If using a separate token server, make sure CORS headers are set:
  ```javascript
  res.setHeader('Access-Control-Allow-Origin', '*')
  res.setHeader('Access-Control-Allow-Methods', 'POST')
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type')
  ```

### 4. Wrong API Endpoint Path

**Symptom**: 404 error, endpoint not found

**For Vercel**:
- Endpoint should be: `https://your-app.vercel.app/api/token`
- Make sure `vercel.json` has the correct rewrite rules

**For Netlify**:
- Endpoint should be: `https://your-app.netlify.app/.netlify/functions/token`
- Make sure `netlify.toml` has the correct redirects

**Solution**:
- Test the endpoint directly:
  ```bash
  curl -X POST https://your-app.vercel.app/api/token \
    -H "Content-Type: application/json" \
    -d '{"room":"test","participant":"test-user"}'
  ```

### 5. Missing Dependencies

**Symptom**: Token API build fails or runtime error

**For Vercel**:
- Make sure `@vercel/node` and `livekit-server-sdk` are in `package.json`
- Add to `frontend/package.json`:
  ```json
  {
    "dependencies": {
      "@vercel/node": "^3.0.0",
      "livekit-server-sdk": "^2.0.0"
    }
  }
  ```

**For Netlify**:
- Make sure `livekit-server-sdk` is in `package.json`
- Netlify automatically installs dependencies

**Solution**:
1. Add missing dependencies to `package.json`
2. Run `npm install` locally to verify
3. Redeploy

### 6. Local Development Issues

**Symptom**: Works in production but not locally

**Solution**:
- For local development, you need to run a token server
- Option 1: Use the token server in `frontend/server.js`:
  ```bash
  cd frontend
  node server.js
  ```
- Option 2: Update `App.tsx` to use a local token server:
  ```typescript
  const tokenUrl = import.meta.env.DEV 
    ? 'http://localhost:3001/api/token'
    : '/api/token'
  ```

## Debugging Steps

### Step 1: Check Browser Console

1. Open browser DevTools (F12)
2. Go to **Console** tab
3. Look for error messages when clicking "Start Voice Call"
4. Check **Network** tab for the `/api/token` request:
   - Status code
   - Response body
   - Request headers

### Step 2: Check Deployment Logs

**Vercel**:
1. Go to Vercel dashboard
2. Click on your project
3. Go to **Deployments** tab
4. Click on latest deployment
5. Check **Function Logs** for errors

**Netlify**:
1. Go to Netlify dashboard
2. Click on your site
3. Go to **Functions** tab
4. Check logs for the `token` function

### Step 3: Test Token API Directly

Test the endpoint with curl:

```bash
# For Vercel
curl -X POST https://your-app.vercel.app/api/token \
  -H "Content-Type: application/json" \
  -d '{"room":"test-room","participant":"test-user"}'

# For Netlify
curl -X POST https://your-app.netlify.app/.netlify/functions/token \
  -H "Content-Type: application/json" \
  -d '{"room":"test-room","participant":"test-user"}'
```

**Expected Response**:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "url": "wss://your-livekit-server.com"
}
```

**If you get an error**, check:
- Environment variables are set
- API key/secret are correct
- LiveKit URL is correct

### Step 4: Verify Environment Variables

**Vercel**:
1. Go to **Settings** → **Environment Variables**
2. Verify these are set:
   - `LIVEKIT_URL`
   - `LIVEKIT_API_KEY`
   - `LIVEKIT_API_SECRET`
3. Make sure they're set for the correct environment (Production/Preview/Development)

**Netlify**:
1. Go to **Site settings** → **Environment variables**
2. Verify the same variables are set

### Step 5: Check Token API Code

Make sure `frontend/api/token.ts` (Vercel) or `frontend/netlify/functions/token.js` (Netlify) exists and has the correct code.

## Quick Fix Checklist

- [ ] Environment variables are set in deployment platform
- [ ] Environment variables are set for all environments (Production/Preview/Development)
- [ ] Token API file exists in correct location
- [ ] Dependencies are installed (`@vercel/node`, `livekit-server-sdk`)
- [ ] Deployment was successful (check logs)
- [ ] Token API endpoint is accessible (test with curl)
- [ ] Browser console shows detailed error messages
- [ ] CORS is configured (if using separate server)

## Still Having Issues?

1. **Check deployment logs** for specific errors
2. **Test token API directly** with curl
3. **Verify environment variables** are set correctly
4. **Check browser console** for detailed error messages
5. **Try redeploying** after fixing issues

## Common Error Messages

### "LiveKit configuration missing"
- **Cause**: Environment variables not set
- **Fix**: Add `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET` to deployment environment variables

### "Method not allowed"
- **Cause**: Token API only accepts POST requests
- **Fix**: Make sure frontend sends POST request (should be automatic)

### "Room and participant are required"
- **Cause**: Request body missing required fields
- **Fix**: Check that frontend sends `room` and `participant` in request body

### "Failed to reach token API"
- **Cause**: Network error or endpoint not accessible
- **Fix**: Check endpoint URL, verify deployment, check CORS settings
