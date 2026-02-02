# Beyond Presence Concurrency Limit - Workaround

## Issue
Beyond Presence returns a 429 error when you've reached your concurrency limit:
```
APIStatusError: Server returned an error (status_code=429, ...)
{"detail":"You have reached your concurrency limit. Please upgrade your plan or stop other ongoing sessions."}
```

## Solution Implemented

The code now includes **graceful fallback** to placeholder video when Beyond Presence is unavailable:

1. **Detects concurrency limit errors** (429 status code)
2. **Logs helpful error messages** with solutions
3. **Automatically falls back to placeholder video** so the agent still works
4. **Continues normal operation** - voice agent works, just with placeholder avatar

## How It Works

### When Beyond Presence Fails:
1. Backend detects the 429 error
2. Logs warning with solutions
3. Automatically enables placeholder video as fallback
4. Agent continues working normally

### What You'll See:
- **Backend logs**: Warning about concurrency limit + fallback message
- **Frontend**: Placeholder avatar video (animated test pattern)
- **Voice agent**: Works normally (audio, transcription, tool calls all work)

## Permanent Solutions

### Option 1: Stop Other Sessions
1. Go to [Beyond Presence Dashboard](https://app.bey.chat)
2. Check for active/ongoing sessions
3. End sessions you're not using
4. Restart your backend agent

### Option 2: Upgrade Plan
1. Go to Beyond Presence billing/subscription page
2. Upgrade to a plan with higher concurrency limits
3. Restart your backend agent

### Option 3: Wait
- If you have other sessions running, wait for them to complete
- Then restart your backend agent

## Testing the Fallback

The fallback is automatic. To test:

1. **Start backend agent** with Beyond Presence configured
2. **If concurrency limit hit**: You'll see placeholder video
3. **If limit resolved**: Real avatar will work

## Disable Fallback (Optional)

If you don't want placeholder video when Beyond Presence fails, you can:

1. Set `ENABLE_AVATAR_VIDEO=false` in `backend/.env`
2. Agent will work without any video (audio-only)

## Current Behavior

✅ **Voice agent works** - All functionality intact  
✅ **Placeholder video** - Shows animated test pattern  
✅ **Clear error messages** - Knows what went wrong  
✅ **Graceful degradation** - System doesn't crash  

Once you resolve the concurrency limit, the real Beyond Presence avatar will automatically work on the next restart.
