# Alternative: Move API to Project Root

If the token API still returns 404 after updating `vercel.json`, try this alternative approach:

## Option 1: Move API to Project Root (Recommended if above doesn't work)

1. **Move the API folder**:
   ```bash
   # From project root
   mv frontend/api api
   ```

2. **Update Vercel settings**:
   - **Root Directory**: (leave empty or set to project root)
   - **Build Command**: `cd frontend && npm run build`
   - **Output Directory**: `frontend/dist`

3. **Update vercel.json** (at project root):
   ```json
   {
     "functions": {
       "api/token.ts": {
         "runtime": "@vercel/node"
       }
     }
   }
   ```

4. **Redeploy**

## Option 2: Keep API in Frontend, Update Vercel Settings

If you want to keep `api` in `frontend`:

1. **In Vercel dashboard**:
   - Go to Settings → General
   - Make sure **Root Directory** is set to `frontend`
   - Verify **Build Command** is `npm run build`
   - Verify **Output Directory** is `dist`

2. **Check Functions tab**:
   - After deployment, go to Functions tab
   - You should see `api/token` listed
   - If not, check deployment logs for errors

3. **Verify file is in git**:
   - Make sure `frontend/api/token.ts` is committed
   - Push to GitHub if not already

## Option 3: Use Netlify Instead

If Vercel continues to have issues, you can use Netlify:

1. **Deploy to Netlify** instead of Vercel
2. **Netlify automatically detects** `netlify/functions/token.js`
3. **Endpoint will be**: `https://your-app.netlify.app/.netlify/functions/token`
4. **Update frontend** to use Netlify endpoint if needed

## Quick Test

After redeploying, test with:
```bash
curl -X POST https://your-app.vercel.app/api/token \
  -H "Content-Type: application/json" \
  -d '{"room":"test","participant":"test-user"}'
```

Expected: JSON response with `token` and `url` fields
Error: 404 means function not found, 500 means env vars missing
