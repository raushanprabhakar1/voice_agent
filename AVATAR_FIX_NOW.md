# Fix Avatar Video Track Issue - RIGHT NOW

## The Problem

Frontend shows: `hasVideoTrack: false` - backend is not publishing video tracks.

## Immediate Fix

### Step 1: Set Environment Variable

**CRITICAL**: Add this to `backend/.env`:

```env
ENABLE_AVATAR_VIDEO=true
AVATAR_PROVIDER=placeholder
```

### Step 2: Verify .env File

Make sure the file exists and has the correct values:

```bash
cd backend
cat .env | grep -E "ENABLE_AVATAR|AVATAR_PROVIDER"
```

Should show:
```
ENABLE_AVATAR_VIDEO=true
AVATAR_PROVIDER=placeholder
```

### Step 3: Restart Backend Agent

**IMPORTANT**: Environment variables are only loaded when the agent starts!

1. **Stop** the backend (Ctrl+C)
2. **Start** it again:
   ```bash
   cd backend
   ./venv/bin/python -m livekit.agents dev agent.py
   ```

### Step 4: Check Backend Logs

Look for these messages when the agent starts:

**✅ SUCCESS - You should see:**
```
Avatar video enabled check: True
Will publish avatar video after session starts (provider: placeholder)
...
Publishing avatar video track (provider: placeholder)...
Creating avatar video track: 1280x720 @ 30fps (provider: placeholder)
✅ Published avatar video track (1280x720 @ 30fps)
Generating placeholder avatar video frames
```

**❌ FAILURE - If you see:**
```
Avatar video disabled - set ENABLE_AVATAR_VIDEO=true to enable
```
→ The environment variable is NOT being read. Check your `.env` file location and restart.

### Step 5: Check Frontend

After connecting, frontend console should show:
```
Track published: video from agent-[ID]
Video track published, subscribing...
Video track received from agent
AvatarPlayer: Attaching video track to element
```

## Why This Happens

The code checks `ENABLE_AVATAR_VIDEO` environment variable. If it's:
- Not set → defaults to `false` → video disabled
- Set to anything other than `"true"` → video disabled
- Set correctly but agent not restarted → old value still in memory

## Quick Test

Run this to verify your environment:

```bash
cd backend
python3 -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('ENABLE_AVATAR_VIDEO:', os.getenv('ENABLE_AVATAR_VIDEO'))
print('AVATAR_PROVIDER:', os.getenv('AVATAR_PROVIDER'))
print('Should be: ENABLE_AVATAR_VIDEO=true, AVATAR_PROVIDER=placeholder')
"
```

If it doesn't show `true` and `placeholder`, your `.env` file is not being read correctly.

## Still Not Working?

1. **Check .env file location** - should be in `backend/.env` (same directory as `agent.py`)
2. **Check .env file format** - no spaces around `=`, no quotes needed:
   ```env
   ENABLE_AVATAR_VIDEO=true
   ```
   NOT:
   ```env
   ENABLE_AVATAR_VIDEO = "true"  # Wrong!
   ```
3. **Restart backend** - environment variables only load on startup
4. **Check backend logs** - look for "Avatar video" messages

## Expected Behavior

Once working:
- Backend logs show "✅ Published avatar video track"
- Frontend console shows "Video track received from agent"
- You see animated gradient pattern video in the UI
