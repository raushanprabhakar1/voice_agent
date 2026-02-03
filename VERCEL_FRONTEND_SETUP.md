# Vercel Frontend Setup - Step by Step

## Issue

Can't find where to set "Framework Preset" and "Root Directory" in Vercel.

## Solution

Vercel's interface has changed. Here's the updated process:

## Step-by-Step Vercel Configuration

### Step 1: Import Project

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click **"Add New Project"** (or **"Import Project"**)
3. Select your GitHub repository
4. Click **"Import"**

### Step 2: Configure Project Settings

After importing, you'll see the **"Configure Project"** page. Here's what to set:

#### Option A: If you see "Framework Preset" dropdown

1. **Framework Preset**: 
   - Look for a dropdown that says "Framework Preset" or "Framework"
   - Select **"Vite"** from the dropdown
   - (If Vite is not listed, select "Other" or "Other" and it will auto-detect)

2. **Root Directory**:
   - Look for "Root Directory" field
   - Click "Edit" or the folder icon next to it
   - Type: `frontend`
   - Or click "Browse" and select the `frontend` folder

3. **Build and Output Settings**:
   - **Build Command**: Should auto-fill as `npm run build` (if not, set it manually)
   - **Output Directory**: Should auto-fill as `dist` (if not, set it manually)
   - **Install Command**: Should auto-fill as `npm install` (if not, set it manually)

#### Option B: If you DON'T see "Framework Preset" (New Vercel UI)

1. **Root Directory**:
   - Look for a field labeled **"Root Directory"** or **"Project Root"**
   - It might be under "Advanced" or "Settings"
   - Click on it and type: `frontend`
   - Or use the folder picker to select the `frontend` folder

2. **Build Settings**:
   - Vercel should auto-detect Vite
   - If not, you can manually set:
     - **Build Command**: `cd frontend && npm run build`
     - **Output Directory**: `frontend/dist`
     - **Install Command**: `cd frontend && npm install`

### Step 3: Alternative Method (If Above Doesn't Work)

If you can't find these settings during import:

1. **Import the project first** (even if settings aren't perfect)
2. After import, go to your **project dashboard**
3. Click on **"Settings"** tab
4. Click on **"General"** in the left sidebar
5. Scroll down to find:
   - **Root Directory**: Set to `frontend`
   - **Build & Development Settings**: 
     - Framework Preset: Vite
     - Build Command: `npm run build`
     - Output Directory: `dist`
     - Install Command: `npm install`

### Step 4: Environment Variables

**Before deploying**, add environment variables:

1. On the "Configure Project" page, look for **"Environment Variables"** section
2. Or after importing, go to **Settings** → **Environment Variables**
3. Add these variables:

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
- Add these for **Production**, **Preview**, and **Development** environments
- Or at least add them for **Production**

### Step 5: Deploy

1. Click **"Deploy"** button
2. Wait for build to complete (usually 1-2 minutes)
3. Your site will be live!

## Visual Guide

### Where to Find Settings

**During Import:**
```
┌─────────────────────────────────────┐
│ Configure Project                   │
├─────────────────────────────────────┤
│ Framework Preset: [Vite ▼]         │
│ Root Directory: [frontend]          │
│ Build Command: [npm run build]      │
│ Output Directory: [dist]            │
│                                     │
│ Environment Variables               │
│ [Add Variable]                      │
│                                     │
│ [Deploy]                            │
└─────────────────────────────────────┘
```

**After Import (Settings Page):**
```
Settings → General
├── Project Name
├── Framework: Vite
├── Root Directory: frontend
└── Build & Development Settings
    ├── Build Command: npm run build
    ├── Output Directory: dist
    └── Install Command: npm install
```

## Troubleshooting

### Can't Find Root Directory Setting

**Solution 1**: Use the folder structure approach
- Make sure your repo structure is:
  ```
  your-repo/
  └── frontend/
      ├── package.json
      ├── vite.config.ts
      └── src/
  ```
- Then set Root Directory to: `frontend`

**Solution 2**: Use build commands with `cd`
- Set Build Command to: `cd frontend && npm run build`
- Set Output Directory to: `frontend/dist`
- Set Install Command to: `cd frontend && npm install`

### Vite Not Detected

If Vercel doesn't auto-detect Vite:
1. Go to Settings → General
2. Under "Framework Preset", select "Vite"
3. Or select "Other" and it should still work

### Build Fails

If build fails:
1. Check that `frontend/package.json` exists
2. Check that `frontend/vite.config.ts` exists
3. Verify Root Directory is set to `frontend`
4. Check build logs for specific errors

## Quick Fix: Manual Configuration

If you're stuck, here's the manual approach:

1. **Import project** (use default settings)
2. Go to **Settings** → **General**
3. Set **Root Directory**: `frontend`
4. Go to **Settings** → **Build & Development Settings**
5. Set:
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`
6. Go to **Settings** → **Environment Variables**
7. Add all required variables
8. Go to **Deployments** tab
9. Click **"Redeploy"** on the latest deployment

## Still Having Issues?

If you still can't find these settings:

1. **Take a screenshot** of your Vercel "Configure Project" page
2. **Check Vercel's documentation**: [vercel.com/docs](https://vercel.com/docs)
3. **Try the Vercel CLI**:
   ```bash
   npm i -g vercel
   cd frontend
   vercel
   ```
   This will guide you through setup interactively

## Success Indicators

After successful deployment, you should see:
- ✅ Build completed successfully
- ✅ Deployment URL (e.g., `https://your-project.vercel.app`)
- ✅ "Ready" status
- ✅ No build errors in logs

Your frontend is now live! 🎉
