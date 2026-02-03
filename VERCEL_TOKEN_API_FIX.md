# Vercel Token API 404 Fix

## Issue

Getting 404 error: "Token API endpoint was not found"

## Solution

The token API file exists at `frontend/api/token.ts`, but Vercel might not be recognizing it. Here are the fixes:

### Fix 1: Update vercel.json (Already Done)

I've updated `vercel.json` to explicitly configure the token API function:

```json
{
  "functions": {
    "api/token.ts": {
      "runtime": "@vercel/node"
    }
  },
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "/api/:path*"
    }
  ]
}
```

### Fix 2: Verify File Structure

Make sure your file structure is:
```
frontend/
├── api/
│   └── token.ts    ← This file must exist
├── vercel.json     ← Configuration file
└── package.json    ← Must include @vercel/node
```

### Fix 3: Check Vercel Settings

1. **Root Directory**: Should be set to `frontend` in Vercel project settings
2. **Build Command**: `npm run build`
3. **Output Directory**: `dist`
4. **Install Command**: `npm install`

### Fix 4: Verify Dependencies

Make sure `package.json` includes:
```json
{
  "dependencies": {
    "livekit-server-sdk": "^2.0.0"
  },
  "devDependencies": {
    "@vercel/node": "^3.0.0"
  }
}
```

### Fix 5: Redeploy

After making changes:
1. Commit and push to GitHub
2. Vercel will auto-deploy
3. Or manually trigger a redeploy in Vercel dashboard

### Fix 6: Check Deployment Logs

1. Go to Vercel dashboard
2. Click on your project
3. Go to **Deployments** tab
4. Click on latest deployment
5. Check **Function Logs** to see if `api/token.ts` was built

You should see something like:
```
Building functions...
api/token.ts
```

### Fix 7: Test After Deployment

After redeploying, test the endpoint:
```bash
curl -X POST https://your-app.vercel.app/api/token \
  -H "Content-Type: application/json" \
  -d '{"room":"test","participant":"test-user"}'
```

### Alternative: Move API Folder (If Above Doesn't Work)

If the above doesn't work, you can try moving the API to the project root:

1. Move `frontend/api/token.ts` to `api/token.ts` (project root)
2. Update Vercel root directory to project root (not `frontend`)
3. Update build settings:
   - **Root Directory**: (empty or project root)
   - **Build Command**: `cd frontend && npm run build`
   - **Output Directory**: `frontend/dist`

But this is usually not necessary - the first approach should work.

## Verification Checklist

- [ ] `frontend/api/token.ts` exists
- [ ] `frontend/vercel.json` has functions configuration
- [ ] `@vercel/node` is in `package.json` devDependencies
- [ ] `livekit-server-sdk` is in `package.json` dependencies
- [ ] Environment variables are set in Vercel
- [ ] Root directory is set to `frontend` in Vercel
- [ ] Deployment logs show function was built
- [ ] Test endpoint with curl returns 200 (not 404)

## Still Getting 404?

1. **Check Vercel Functions tab**:
   - Go to Vercel dashboard → Your project → Functions tab
   - You should see `api/token` listed
   - If not, the function wasn't built

2. **Check build logs**:
   - Look for errors during function build
   - Make sure TypeScript compiles without errors

3. **Try manual function test**:
   - In Vercel dashboard, go to Functions tab
   - Click on `api/token` if it exists
   - Test it directly from there

4. **Verify file is committed**:
   - Make sure `frontend/api/token.ts` is in your git repo
   - Push to GitHub if not already pushed
   - Vercel only deploys what's in git
