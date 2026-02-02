# Get Avatar Working - Step by Step

## Quick Fix: Use Placeholder Video (Works Immediately)

This is the simplest way to get video working right now:

### Step 1: Backend Configuration

Add to `backend/.env`:
```env
ENABLE_AVATAR_VIDEO=true
AVATAR_PROVIDER=placeholder
```

### Step 2: Frontend Configuration

Add to `frontend/.env`:
```env
VITE_AVATAR_PROVIDER=livekit-video
```

### Step 3: Restart Everything

1. **Stop your backend agent** (Ctrl+C)
2. **Restart backend**:
   ```bash
   cd backend
   ./venv/bin/python -m livekit.agents dev agent.py
   ```

3. **Restart frontend** (if running):
   ```bash
   cd frontend
   npm run dev
   ```

### Step 4: Check Logs

**Backend should show**:
```
✅ Published avatar video track (1280x720 @ 30fps)
Generating placeholder avatar video frames
```

**Frontend console should show**:
```
Video track received from agent
Video track published, subscribing...
AvatarPlayer: Attaching video track to element
AvatarPlayer: Video track attached successfully
```

### Step 5: Test

1. Connect to the agent from frontend
2. You should see an **animated gradient pattern** (test video)
3. This confirms the video pipeline is working!

## If Placeholder Doesn't Work

### Check 1: Environment Variables

Run this to check your config:
```bash
cd backend
python3 test_avatar.py
```

Or manually check:
```bash
# Backend
grep ENABLE_AVATAR_VIDEO backend/.env
grep AVATAR_PROVIDER backend/.env

# Frontend  
grep VITE_AVATAR_PROVIDER frontend/.env
```

### Check 2: Backend Logs

Look for these messages when agent starts:
- `Creating avatar video track: 1280x720 @ 30fps`
- `✅ Published avatar video track`
- `Generating placeholder avatar video frames`

If you see errors, share them.

### Check 3: Frontend Console

Open browser DevTools (F12) and check Console tab:
- Should see: `Video track received from agent`
- Should see: `AvatarPlayer: Video track attached successfully`

If you see errors, share them.

### Check 4: Video Element

In browser console, run:
```javascript
const video = document.querySelector('.avatar-video');
console.log('Video element:', video);
console.log('Video srcObject:', video?.srcObject);
console.log('Video readyState:', video?.readyState);
```

## Common Issues

### Issue: "Avatar video disabled"

**Fix**: Set `ENABLE_AVATAR_VIDEO=true` in `backend/.env`

### Issue: "No video track received"

**Fix**: 
1. Check backend logs for "Published avatar video track"
2. Verify `VITE_AVATAR_PROVIDER=livekit-video` in frontend
3. Check network connection

### Issue: "Video element not available"

**Fix**: 
1. Refresh the page
2. Check that AvatarPlayer component is rendering
3. Check browser console for React errors

### Issue: Video is black/not playing

**Fix**:
1. Check that frames are being generated (look for "Captured frame" in backend logs)
2. Check browser console for video playback errors
3. Try reducing resolution:
   ```env
   AVATAR_VIDEO_WIDTH=640
   AVATAR_VIDEO_HEIGHT=360
   ```

## Next: Real Avatar Integration

Once placeholder video works, you can integrate real avatars:

### For Tavus:

1. **Install plugin**:
   ```bash
   cd backend
   ./venv/bin/pip install 'livekit-agents[tavus]'
   ```

2. **Get credentials** from Tavus dashboard

3. **Update `backend/.env`**:
   ```env
   ENABLE_AVATAR_VIDEO=false  # Disable placeholder
   AVATAR_PROVIDER=tavus
   TAVUS_API_KEY=your-key
   TAVUS_REPLICA_ID=your-replica-id
   TAVUS_PERSONA_ID=your-persona-id
   ```

4. **Restart backend**

### For Beyond Presence:

1. **Install plugin**:
   ```bash
   ./venv/bin/pip install 'livekit-agents[beyond-presence]'
   ```

2. **Update `backend/.env`**:
   ```env
   ENABLE_AVATAR_VIDEO=false
   AVATAR_PROVIDER=beyond-presence
   BEYOND_PRESENCE_API_KEY=your-key
   BEYOND_PRESENCE_AVATAR_ID=your-avatar-id
   ```

## Still Not Working?

Share:
1. **Backend logs** (especially around "avatar" or "video")
2. **Frontend console** errors
3. **Environment variables** you've set (without sensitive values)
4. **What you see** (black screen, no video element, error messages, etc.)

This will help identify the exact issue!
