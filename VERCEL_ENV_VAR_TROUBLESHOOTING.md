# 🔧 Vercel Environment Variables Troubleshooting

## Error: FUNCTION_INVOCATION_FAILED

If you're seeing `FUNCTION_INVOCATION_FAILED` even though you've set environment variables, follow these steps:

## Step 1: Verify Environment Variables Are Set Correctly

### Check Variable Names (Case-Sensitive!)
Make sure the variable names are **exactly**:
- `LIVEKIT_API_KEY` (not `livekit_api_key` or `LIVEKIT-API-KEY`)
- `LIVEKIT_API_SECRET` (not `livekit_api_secret` or `LIVEKIT-API-SECRET`)
- `LIVEKIT_URL` (not `livekit_url` or `LIVEKIT-URL`)

### Check Which Environment They're Set For

**Critical**: Vercel has separate environments:
- **Production** - Your main deployed site
- **Preview** - Preview deployments (from pull requests)
- **Development** - Local development

**You must set variables for the environment you're using!**

1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
2. For each variable, check which environments are selected:
   - If you're on Production, make sure **Production** is checked ✅
   - If you're on a Preview deployment, make sure **Preview** is checked ✅
   - If testing locally, make sure **Development** is checked ✅

**Common Mistake**: Variables set only for "Development" won't work in Production!

## Step 2: Check Variable Values

### Verify No Extra Spaces
- Make sure there are no leading/trailing spaces in the values
- Copy the values directly from your LiveKit dashboard (don't type them)

### Verify Format
- **LIVEKIT_API_KEY**: Usually starts with `AP...` (e.g., `APxxxxxxxxxxxxx`)
- **LIVEKIT_API_SECRET**: A long string (usually 40+ characters)
- **LIVEKIT_URL**: Should start with `wss://` (e.g., `wss://your-project.livekit.cloud`)

### Common Issues:
❌ `wss://your-project.livekit.cloud ` (trailing space)
❌ ` wss://your-project.livekit.cloud` (leading space)
❌ `https://your-project.livekit.cloud` (wrong protocol - should be `wss://`)
✅ `wss://your-project.livekit.cloud` (correct)

## Step 3: Redeploy After Setting Variables

**Important**: After adding or changing environment variables, you MUST redeploy!

1. Go to **Deployments** tab
2. Click the **⋯** (three dots) on the latest deployment
3. Click **Redeploy**
4. Wait for deployment to complete

**Why?** Environment variables are injected at build/deploy time, not at runtime. Old deployments won't have new variables.

## Step 4: Check Function Logs

1. Go to Vercel Dashboard → Your Project → Deployments
2. Click on the latest deployment
3. Click on **Functions** tab (or look for function logs)
4. Find the `/api/token` function
5. Check the logs for:
   - Environment variable check messages
   - Error messages
   - Which variables are missing

The improved error handling will now show:
- Which variables are present/missing
- Length of each variable (to detect empty strings)
- More detailed error messages

## Step 5: Test the Function Directly

Test the endpoint with curl to see the actual error:

```bash
curl -X POST https://your-project.vercel.app/api/token \
  -H "Content-Type: application/json" \
  -d '{"room":"test-room","participant":"test-user"}'
```

This will show you the exact error message from the function.

## Step 6: Verify Root Directory Configuration

If your root directory is set to `frontend`, make sure:
- The API file is at: `frontend/api/token.ts`
- The `package.json` is at: `frontend/package.json`
- Environment variables are set at the **project level** (not function level)

## Common Scenarios

### Scenario 1: Variables Set But Function Still Fails

**Possible Causes:**
1. Variables set for wrong environment (e.g., only Development but using Production)
2. Variables have typos in names
3. Variables have extra spaces
4. Didn't redeploy after setting variables

**Solution:**
- Double-check variable names (case-sensitive!)
- Verify environment selection
- Redeploy

### Scenario 2: Works Locally But Not in Production

**Cause**: Variables only set for Development environment

**Solution**: 
- Go to Environment Variables
- For each variable, click "Edit"
- Make sure **Production** is checked
- Redeploy

### Scenario 3: Works in Preview But Not Production

**Cause**: Variables only set for Preview environment

**Solution**:
- Set variables for Production environment
- Redeploy

## Quick Checklist

- [ ] Variable names are exactly: `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`, `LIVEKIT_URL`
- [ ] Variables are set for the correct environment (Production/Preview/Development)
- [ ] No extra spaces in variable values
- [ ] LIVEKIT_URL starts with `wss://` (not `https://`)
- [ ] Redeployed after setting/changing variables
- [ ] Checked function logs for detailed error messages
- [ ] Tested endpoint directly with curl

## Still Not Working?

1. **Check Vercel Function Logs**:
   - Go to Deployments → Latest → Functions → `/api/token`
   - Look for the debug messages showing which variables are present

2. **Verify in Vercel Dashboard**:
   - Settings → Environment Variables
   - Make sure all three variables are listed
   - Check the environment checkboxes

3. **Try Setting Variables Again**:
   - Delete the variables
   - Add them again (one by one)
   - Make sure to select the correct environment
   - Redeploy

4. **Check for Typos**:
   - Copy variable names from this guide
   - Don't type them manually

5. **Contact Support**:
   - If everything looks correct but still fails
   - Share the function logs with Vercel support
