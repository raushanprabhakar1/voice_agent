# Avatar Debugging - Video Track Not Appearing

## Current Issue

Frontend shows: `hasVideoTrack: false` - meaning no video track is being received from the backend.

## Quick Fix Steps

### 1. Verify Backend Environment Variable

**CRITICAL**: Make sure `ENABLE_AVATAR_VIDEO=true` is set in `backend/.env`

Check your `.env` file:
```bash
cd backend
cat .env | grep ENABLE_AVATAR_VIDEO
```

If it's not there or set to `false`, add/update:
```env
ENABLE_AVATAR_VIDEO=true
AVATAR_PROVIDER=placeholder
```

### 2. Check Backend Logs

When you start the backend agent, look for these messages:

**✅ Good signs:**
```
Publishing avatar video track (provider: placeholder)...
Creating avatar video track: 1280x720 @ 30fps (provider: placeholder)
✅ Published avatar video track (1280x720 @ 30fps)
Generating placeholder avatar video frames
```

**❌ Bad signs:**
```
Avatar video disabled (set ENABLE_AVATAR_VIDEO=true to enable)
Avatar video not enabled (set ENABLE_AVATAR_VIDEO=true to enable)
Failed to publish avatar video track: [error message]
```

### 3. Restart Backend After Setting Environment Variable

**Important**: After adding/changing `.env` file:
1. **Stop the backend agent** (Ctrl+C)
2. **Restart it** - environment variables are only loaded on startup

```bash
cd backend
./venv/bin/python -m livekit.agents dev agent.py
```

### 4. Verify Frontend Configuration

In `frontend/.env`:
```env
VITE_AVATAR_PROVIDER=livekit-video
```

### 5. Check Frontend Console

After connecting, you should see:
```
Track published: video from agent-[ID]
Video track published, subscribing...
Video track received from agent
AvatarPlayer: Attaching video track to element
```

## Common Issues

### Issue: "Avatar video disabled" in logs

**Cause**: `ENABLE_AVATAR_VIDEO` is not set to `true`

**Fix**: 
1. Add `ENABLE_AVATAR_VIDEO=true` to `backend/.env`
2. Restart backend agent

### Issue: No video track published message

**Cause**: Video publishing code not running or failing silently

**Fix**:
1. Check backend logs for any errors
2. Verify `avatar_video.py` module exists
3. Check if there are import errors

### Issue: Video track published but frontend doesn't receive it

**Cause**: Subscription issue or timing problem

**Fix**:
1. Check frontend console for subscription errors
2. Verify `VITE_AVATAR_PROVIDER=livekit-video` is set
3. Try refreshing the page after connecting

## Debug Commands

### Check Environment Variables

```bash
# Backend
cd backend
python3 -c "import os; from dotenv import load_dotenv; load_dotenv(); print('ENABLE_AVATAR_VIDEO:', os.getenv('ENABLE_AVATAR_VIDEO')); print('AVATAR_PROVIDER:', os.getenv('AVATAR_PROVIDER'))"
```

### Test Video Publishing

The code now publishes video tracks **after** the session starts to ensure the room is fully connected. Check logs for:
- "Publishing avatar video track (provider: placeholder)..."
- "✅ Published avatar video track"

## Still Not Working?

Share these details:

1. **Backend logs** - especially lines with:
   - "Avatar video"
   - "Published avatar video track"
   - Any errors

2. **Frontend console** - all messages related to:
   - "Track published"
   - "Video track"
   - Any errors

3. **Your `.env` files** (without sensitive values):
   ```bash
   # Backend
   grep -E "ENABLE_AVATAR|AVATAR_PROVIDER" backend/.env
   
   # Frontend
   grep VITE_AVATAR frontend/.env
   ```
