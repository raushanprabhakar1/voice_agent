# Fix Vercel 404 Error for Token API

## Issue

Getting 404 error: "Token API endpoint was not found"

## Root Cause

When Vercel's root directory is set to `frontend`, it might not automatically detect the `api` folder. We need to ensure:

1. `@vercel/node` is in `dependencies` (not `devDependencies`)
2. `vercel.json` correctly configures the function
3. The file is in the correct location

## Solution Applied

I've made these changes:

1. **Moved `@vercel/node` to dependencies** in `package.json`
2. **Simplified `vercel.json`** to explicitly configure the function

## Next Steps

### Step 1: Commit and Push Changes

```bash
git add frontend/package.json frontend/vercel.json
git commit -m "Fix Vercel token API configuration"
git push
```

### Step 2: Redeploy in Vercel

1. Go to Vercel dashboard
2. Click on your project
3. Click **"Redeploy"** on the latest deployment
4. Or wait for auto-deploy after push

### Step 3: Verify Function is Built

1. Go to Vercel dashboard → Your project
2. Click **"Functions"** tab
3. You should see `api/token` listed
4. If not, check **Deployment Logs** for errors

### Step 4: Test the Endpoint

After redeploying, test:
```bash
curl -X POST https://your-app.vercel.app/api/token \
  -H "Content-Type: application/json" \
  -d '{"room":"test","participant":"test-user"}'
```

## Alternative Solution (If Still Doesn't Work)

If you still get 404 after the above, try moving the API to project root:

### Option A: Move API to Project Root

1. **Move the API folder**:
   ```bash
   # From project root
   mv frontend/api api
   ```

2. **Update Vercel Settings**:
   - **Root Directory**: (empty - use project root)
   - **Build Command**: `cd frontend && npm run build`
   - **Output Directory**: `frontend/dist`

3. **Create `vercel.json` at project root**:
   ```json
   {
     "functions": {
       "api/token.ts": {
         "runtime": "@vercel/node"
       }
     }
   }
   ```

4. **Update `frontend/package.json`** to include `@vercel/node` in dependencies (already done)

5. **Redeploy**

### Option B: Use Netlify Instead

If Vercel continues to have issues:

1. Deploy to Netlify instead
2. Netlify automatically detects `netlify/functions/token.js`
3. Endpoint: `https://your-app.netlify.app/.netlify/functions/token`
4. Update frontend to use Netlify endpoint if needed

## Verification Checklist

After redeploying:

- [ ] `@vercel/node` is in `dependencies` (not `devDependencies`)
- [ ] `vercel.json` exists and has functions configuration
- [ ] `api/token.ts` file exists in `frontend/api/`
- [ ] Environment variables are set in Vercel
- [ ] Functions tab shows `api/token` after deployment
- [ ] Test endpoint returns 200 (not 404)

## Debugging

### Check Deployment Logs

1. Go to Vercel → Your project → Deployments
2. Click on latest deployment
3. Check **Build Logs** for:
   - Function build errors
   - TypeScript compilation errors
   - Missing dependencies

### Check Functions Tab

1. Go to Vercel → Your project → Functions
2. If `api/token` is listed:
   - Click on it to see details
   - Check for runtime errors
3. If not listed:
   - The function wasn't built
   - Check build logs for errors

### Common Issues

1. **TypeScript errors**: Fix TS errors in `api/token.ts`
2. **Missing dependency**: Make sure `@vercel/node` is installed
3. **Wrong file location**: Make sure `api/token.ts` is in `frontend/api/`
4. **Root directory mismatch**: Make sure Vercel root directory matches file structure
