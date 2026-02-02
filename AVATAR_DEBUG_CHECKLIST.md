# Avatar Debug Checklist

## Issue: Avatar Not Joining Room

If you only see the agent participant but no avatar participant, follow this checklist:

## Backend Configuration

### 1. Check Backend Environment Variables

In `backend/.env`, you MUST have:

```env
AVATAR_PROVIDER=beyond-presence
BEY_API_KEY=your-api-key-here
BEY_AVATAR_ID=your-avatar-id-here
```

**OR** (alternative naming):

```env
AVATAR_PROVIDER=beyond-presence
BEYOND_PRESENCE_API_KEY=your-api-key-here
BEYOND_PRESENCE_AVATAR_ID=your-avatar-id-here
```

### 2. Check Backend Logs

When you start the backend agent, look for these log messages:

**✅ Success messages:**
```
Setting up beyond-presence avatar...
Setting up Beyond Presence avatar - Avatar ID: [your-avatar-id]
✅ Beyond Presence avatar session started successfully
   Avatar will handle audio/video publishing - agent audio will be sent to avatar
```

**❌ Error messages to watch for:**

- `BEY_API_KEY (or BEYOND_PRESENCE_API_KEY) and BEY_AVATAR_ID (or BEYOND_PRESENCE_AVATAR_ID) must be set`
  - **Fix**: Add the missing environment variables to `backend/.env`

- `Beyond Presence plugin not installed`
  - **Fix**: Run `pip install 'livekit-agents[bey]'` in your backend venv

- `Failed to setup Beyond Presence avatar: [error]`
  - **Fix**: Check the error message - might be invalid API key or avatar ID

- `No avatar provider specified, skipping avatar setup`
  - **Fix**: Set `AVATAR_PROVIDER=beyond-presence` in `backend/.env`

- `Avatar session creation failed - continuing without avatar`
  - **Fix**: Check the logs above this message for the specific error

### 3. Verify Plugin Installation

```bash
cd backend
source venv/bin/activate  # or: ./venv/bin/activate
pip list | grep bey
```

You should see: `livekit-plugins-bey` in the list.

If not installed:
```bash
pip install 'livekit-agents[bey]'
```

### 4. Test Environment Variables

Create a test script to verify env vars are loaded:

```bash
cd backend
source venv/bin/activate
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('AVATAR_PROVIDER:', os.getenv('AVATAR_PROVIDER')); print('BEY_API_KEY:', 'SET' if os.getenv('BEY_API_KEY') else 'NOT SET'); print('BEY_AVATAR_ID:', os.getenv('BEY_AVATAR_ID') or 'NOT SET')"
```

## Frontend Configuration

The frontend env vars are optional (just for display). But if you want to set them:

In `frontend/.env`:
```env
VITE_AVATAR_PROVIDER=beyond-presence
VITE_BEYOND_PRESENCE_API_KEY=your-api-key  # Optional
VITE_BEYOND_PRESENCE_AVATAR_ID=your-avatar-id  # Optional
```

## Expected Behavior

### Backend Logs (Success):
1. `Setting up beyond-presence avatar...`
2. `Setting up Beyond Presence avatar - Avatar ID: [id]`
3. `✅ Beyond Presence avatar session started successfully`
4. `Participant connected: [avatar-identity]` (in LiveKit logs)

### Frontend Console (Success):
1. `Participant connected: [avatar-identity]` (different from agent)
2. `Video track published from [avatar-identity], subscribing...`
3. `Video track received from [avatar-identity]`
4. Video appears in the UI

### Current Issue (What You're Seeing):
- Only `Participant connected: agent-AJ_...` (no avatar participant)
- This means the backend avatar session is NOT starting

## Quick Fix Steps

1. **Check backend/.env file exists and has correct values**
2. **Restart backend agent** (env vars are loaded at startup)
3. **Check backend logs** for the success/error messages above
4. **Verify plugin is installed**: `pip list | grep bey`
5. **If still failing, check the specific error message in backend logs**

## Common Issues

### Issue: "BEY_API_KEY must be set"
- **Cause**: Environment variable not set or not loaded
- **Fix**: Add `BEY_API_KEY=...` to `backend/.env` and restart backend

### Issue: "Beyond Presence plugin not installed"
- **Cause**: Plugin not installed in venv
- **Fix**: `pip install 'livekit-agents[bey]'` in backend venv

### Issue: "Avatar session creation failed"
- **Cause**: Invalid API key, invalid avatar ID, or API error
- **Fix**: Verify your Beyond Presence credentials are correct

### Issue: "No avatar provider specified"
- **Cause**: `AVATAR_PROVIDER` not set or set incorrectly
- **Fix**: Set `AVATAR_PROVIDER=beyond-presence` in `backend/.env`
