# Avatar Quick Fix Guide

If you're having trouble running the avatar, follow these steps:

## Option 1: Use Placeholder Video (Simplest - Works Now)

This uses the test pattern video that's already implemented:

1. **Set in `backend/.env`**:
   ```env
   ENABLE_AVATAR_VIDEO=true
   AVATAR_PROVIDER=placeholder
   ```

2. **Set in `frontend/.env`**:
   ```env
   VITE_AVATAR_PROVIDER=livekit-video
   ```

3. **Restart backend agent**:
   ```bash
   cd backend
   ./venv/bin/python -m livekit.agents dev agent.py
   ```

4. **Check logs** for:
   - `✅ Published avatar video track`
   - `Generating placeholder avatar video frames`

5. **Connect from frontend** - you should see animated test pattern video

## Option 2: Use LiveKit Built-in Avatar (Tavus/Beyond Presence)

This requires installing plugins and setting up credentials:

### For Tavus:

1. **Install plugin**:
   ```bash
   cd backend
   ./venv/bin/pip install 'livekit-agents[tavus]'
   ```

2. **Set in `backend/.env`**:
   ```env
   AVATAR_PROVIDER=tavus
   TAVUS_API_KEY=your-api-key
   TAVUS_REPLICA_ID=your-replica-id
   TAVUS_PERSONA_ID=your-persona-id  # Optional
   ```

3. **Restart backend agent**

### For Beyond Presence:

1. **Install plugin**:
   ```bash
   cd backend
   ./venv/bin/pip install 'livekit-agents[beyond-presence]'
   ```

2. **Set in `backend/.env`**:
   ```env
   AVATAR_PROVIDER=beyond-presence
   BEYOND_PRESENCE_API_KEY=your-api-key
   BEYOND_PRESENCE_AVATAR_ID=your-avatar-id
   ```

3. **Restart backend agent**

## Troubleshooting

### No Video Appearing

1. **Check backend logs**:
   - Look for "Published avatar video track" message
   - Check for any errors

2. **Check frontend console**:
   - Look for "Video track received from agent"
   - Check for any errors

3. **Verify environment variables**:
   ```bash
   # Backend
   echo $ENABLE_AVATAR_VIDEO
   echo $AVATAR_PROVIDER
   
   # Frontend
   echo $VITE_AVATAR_PROVIDER
   ```

### Avatar Plugin Not Found

If you see "Avatar plugin not installed":

1. **Install the plugin**:
   ```bash
   cd backend
   ./venv/bin/pip install 'livekit-agents[tavus]'
   # or
   ./venv/bin/pip install 'livekit-agents[beyond-presence]'
   ```

2. **Verify installation**:
   ```bash
   ./venv/bin/pip list | grep livekit
   ```

### Video Track Not Publishing

1. **Check if ENABLE_AVATAR_VIDEO is set**:
   ```bash
   # In backend/.env
   ENABLE_AVATAR_VIDEO=true
   ```

2. **Check backend logs** for errors during video track creation

3. **Try reducing resolution**:
   ```env
   AVATAR_VIDEO_WIDTH=640
   AVATAR_VIDEO_HEIGHT=360
   AVATAR_VIDEO_FPS=15
   ```

## Quick Test

To quickly test if video publishing works:

1. Set `ENABLE_AVATAR_VIDEO=true` and `AVATAR_PROVIDER=placeholder` in backend
2. Set `VITE_AVATAR_PROVIDER=livekit-video` in frontend
3. Restart both
4. Connect - you should see animated gradient pattern

If this works, the video pipeline is working and you can then integrate real avatar services.

## Still Not Working?

1. **Check all logs** (backend and frontend console)
2. **Verify LiveKit connection** is working
3. **Check network** - video requires stable connection
4. **Try the placeholder first** to verify the pipeline works
