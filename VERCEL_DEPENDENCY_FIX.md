# 🔧 Fix: "Cannot find module 'livekit-server-sdk'" in Vercel

## The Problem

Vercel serverless functions can't find `livekit-server-sdk` even though it's in `package.json`.

## Solution Steps

### Step 1: Verify package.json is Committed

Make sure `frontend/package.json` is committed to git:

```bash
git status
# Should show package.json as committed (not in "Untracked files" or "Changes not staged")
```

If not committed:
```bash
git add frontend/package.json
git commit -m "Add livekit-server-sdk dependency"
git push
```

### Step 2: Verify package-lock.json is Committed

Vercel uses `package-lock.json` to ensure exact dependency versions:

```bash
git status
# Should show package-lock.json as committed
```

If not committed:
```bash
cd frontend
npm install  # This will update package-lock.json
git add package-lock.json
git commit -m "Update package-lock.json"
git push
```

### Step 3: Clear Vercel Build Cache

Vercel might be using a cached build without the dependencies:

1. Go to Vercel Dashboard → Your Project → Settings
2. Go to **General** tab
3. Scroll down to **Build & Development Settings**
4. Look for **Clear Build Cache** or **Rebuild** option
5. Or go to **Deployments** → Click **⋯** on latest → **Redeploy** with "Clear Cache" checked

### Step 4: Verify Root Directory is Set Correctly

1. Go to Vercel Dashboard → Your Project → Settings → General
2. Check **Root Directory** is set to: `frontend`
3. If not set, change it to `frontend` and save
4. Redeploy

### Step 5: Check Build Logs

1. Go to Vercel Dashboard → Your Project → Deployments
2. Click on the latest deployment
3. Check the **Build Logs**
4. Look for:
   - `npm install` running
   - `livekit-server-sdk` being installed
   - Any errors during dependency installation

### Step 6: Verify vercel.json Configuration

Make sure `frontend/vercel.json` exists (should have been created):

```json
{
  "functions": {
    "api/token.ts": {
      "includeFiles": "package.json"
    }
  }
}
```

### Step 7: Force Reinstall Dependencies

If still not working, try updating the package.json version to force a rebuild:

1. In `frontend/package.json`, bump the version:
   ```json
   "version": "1.0.1"
   ```
2. Commit and push
3. Vercel will automatically redeploy

## Alternative: Use Explicit Dependency Installation

If the above doesn't work, you can try adding a build script that explicitly installs dependencies:

1. Update `frontend/package.json` scripts:
   ```json
   "scripts": {
     "build": "npm install && tsc && vite build",
     "vercel-build": "npm install && npm run build"
   }
   ```

2. In Vercel Settings → Build & Development Settings:
   - Set **Build Command** to: `npm run vercel-build`

## Verify It's Fixed

After redeploying, check the function logs:

1. Go to Deployments → Latest → Functions → `/api/token`
2. The function should start without "Cannot find module" errors
3. Test the endpoint:
   ```bash
   curl -X POST https://your-project.vercel.app/api/token \
     -H "Content-Type: application/json" \
     -d '{"room":"test","participant":"test-user"}'
   ```

## Common Causes

1. **package.json not committed** - Vercel can't see the dependencies
2. **package-lock.json out of sync** - Dependencies not properly locked
3. **Build cache** - Old build without dependencies
4. **Root directory wrong** - Vercel can't find package.json
5. **Dependencies in devDependencies** - Serverless functions need them in `dependencies`

## Quick Checklist

- [ ] `frontend/package.json` is committed to git
- [ ] `frontend/package-lock.json` is committed to git
- [ ] `livekit-server-sdk` is in `dependencies` (not `devDependencies`)
- [ ] `@vercel/node` is in `dependencies` (not `devDependencies`)
- [ ] Root directory is set to `frontend` in Vercel
- [ ] Cleared build cache / redeployed
- [ ] Checked build logs for `npm install` running
- [ ] `frontend/vercel.json` exists

## Still Not Working?

1. **Check Vercel Build Logs**:
   - Look for `npm install` output
   - Check if `livekit-server-sdk` appears in the install log
   - Look for any errors

2. **Try Manual Installation in Build**:
   - Add to `package.json` scripts:
     ```json
     "vercel-build": "npm install --production=false && npm run build"
     ```
   - Set Build Command in Vercel to: `npm run vercel-build`

3. **Contact Vercel Support**:
   - Share your build logs
   - Share your `package.json`
   - They can help debug dependency installation issues
