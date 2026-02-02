# Avatar Integration Guide

This guide shows you how to integrate real avatars (Tavus or Beyond Presence) with your LiveKit voice agent.

## Quick Start

### Option 1: Using LiveKit's Built-in Avatar Support (Recommended)

This is the easiest and most reliable method. LiveKit handles all the complexity automatically.

#### For Tavus:

1. **Install the Tavus plugin**:
   ```bash
   cd backend
   pip install 'livekit-agents[tavus]'
   ```

2. **Set environment variables** in `backend/.env`:
   ```env
   AVATAR_PROVIDER=tavus
   TAVUS_API_KEY=your-tavus-api-key
   TAVUS_REPLICA_ID=your-replica-id
   TAVUS_PERSONA_ID=your-persona-id  # Optional
   ```

3. **Create Tavus Replica and Persona**:
   - Go to Tavus dashboard
   - Create a Replica (the avatar model)
   - Create a Persona with:
     - `pipeline_mode: echo`
     - `transport_type: livekit`
   - Get the Replica ID and Persona ID

4. **Restart the backend agent** - the avatar will automatically join the room!

#### For Beyond Presence:

1. **Install the Beyond Presence plugin**:
   ```bash
   cd backend
   pip install 'livekit-agents[beyond-presence]'
   ```

2. **Set environment variables** in `backend/.env`:
   ```env
   AVATAR_PROVIDER=beyond-presence
   BEYOND_PRESENCE_API_KEY=your-api-key
   BEYOND_PRESENCE_AVATAR_ID=your-avatar-id
   ```

3. **Restart the backend agent**

### Option 2: Manual Video Frame Generation (Current Implementation)

If you prefer to manually generate video frames (current setup), you can:

1. **Keep using the placeholder** (test pattern):
   ```env
   ENABLE_AVATAR_VIDEO=true
   AVATAR_PROVIDER=placeholder
   ```

2. **Integrate Tavus API directly** in `backend/avatar_video.py`:
   - Update `_generate_tavus_frames()` function
   - Connect to Tavus streaming API
   - Decode video frames and send to `video_source.capture_frame()`

3. **Integrate Beyond Presence API directly**:
   - Update `_generate_beyond_presence_frames()` function
   - Connect to their streaming API
   - Decode video frames and send to `video_source.capture_frame()`

## How It Works

### LiveKit Built-in Integration (Option 1)

When you use LiveKit's built-in avatar support:

1. **AvatarSession** is created with your provider credentials
2. **Avatar worker** automatically joins the room as a separate participant
3. **Audio from agent** is sent to the avatar (not directly to room)
4. **Avatar publishes** synchronized audio + video tracks to the room
5. **Frontend automatically** receives and displays the video

**Benefits:**
- ✅ Automatic synchronization
- ✅ No manual frame generation needed
- ✅ Handles all WebRTC complexity
- ✅ Optimized performance

### Manual Integration (Option 2)

When using manual video frame generation:

1. **Agent publishes video tracks** directly
2. **You generate frames** from avatar API
3. **Frames are captured** to VideoSource
4. **Frontend displays** the video track

**Benefits:**
- ✅ More control over frame generation
- ✅ Can customize frame processing
- ✅ Works with any avatar API

## Frontend Configuration

The frontend automatically handles both approaches. Just set:

```env
# Frontend .env
VITE_AVATAR_PROVIDER=livekit-video
```

The frontend will:
- Automatically detect video tracks from the avatar
- Display them in the AvatarPlayer component
- Sync with speaking state

## Testing

1. **Set up your avatar provider** (Tavus or Beyond Presence)
2. **Configure environment variables**
3. **Restart backend agent**
4. **Connect from frontend**
5. **Check logs** for:
   - `✅ Avatar session started successfully` (Option 1)
   - `✅ Published avatar video track` (Option 2)

## Troubleshooting

### Avatar Not Appearing

1. **Check plugin installation**:
   ```bash
   pip list | grep livekit-agents
   ```

2. **Verify environment variables** are set correctly

3. **Check backend logs** for avatar setup messages

4. **Verify frontend** has `VITE_AVATAR_PROVIDER=livekit-video`

### Audio Issues

- If using Option 1 (built-in), audio is automatically handled
- If using Option 2 (manual), ensure audio is still published from agent

### Video Quality Issues

- Reduce resolution: `AVATAR_VIDEO_WIDTH=640` `AVATAR_VIDEO_HEIGHT=360`
- Reduce frame rate: `AVATAR_VIDEO_FPS=15`

## Next Steps

1. **Choose your approach** (Option 1 recommended)
2. **Install the plugin** for your provider
3. **Set up credentials** in Tavus/Beyond Presence dashboard
4. **Configure environment variables**
5. **Test the integration**

For more details, see:
- [LiveKit Avatar Documentation](https://docs.livekit.io/agents/integrations/avatar)
- [Tavus Integration Guide](https://docs.livekit.io/agents/integrations/avatar/tavus)
