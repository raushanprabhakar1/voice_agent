# Avatar Video Setup Guide

## Quick Start

To enable avatar video publishing from the backend agent:

1. **Set environment variable** in `backend/.env`:
   ```env
   ENABLE_AVATAR_VIDEO=true
   AVATAR_PROVIDER=placeholder
   ```

2. **Optional: Configure video settings**:
   ```env
   AVATAR_VIDEO_WIDTH=1280
   AVATAR_VIDEO_HEIGHT=720
   AVATAR_VIDEO_FPS=30
   ```

3. **Restart the backend agent** - it will now publish video tracks

4. **Frontend will automatically display** the video when `VITE_AVATAR_PROVIDER=livekit-video` is set

## How It Works

1. **Backend** (`backend/avatar_video.py`):
   - Creates a `VideoSource` with specified resolution
   - Creates a `LocalVideoTrack` from the source
   - Publishes the track to the LiveKit room
   - Generates video frames in the background (placeholder or from avatar service)

2. **Frontend** (`frontend/src/components/VoiceAgent.tsx`):
   - Automatically subscribes to video tracks from the agent
   - Displays video in the `AvatarPlayer` component
   - Syncs with speaking state for visual feedback

## Avatar Providers

### Placeholder (Default)

Generates a simple animated test pattern. Good for testing video track publishing.

```env
ENABLE_AVATAR_VIDEO=true
AVATAR_PROVIDER=placeholder
```

### Tavus

To integrate with Tavus:

1. Get your Tavus API key and replica ID
2. Update `_generate_tavus_frames()` in `avatar_video.py` to:
   - Connect to Tavus streaming API
   - Receive video frames
   - Convert to LiveKit VideoFrame format
   - Send to `video_source.capture_frame()`

3. Set environment variables:
   ```env
   ENABLE_AVATAR_VIDEO=true
   AVATAR_PROVIDER=tavus
   TAVUS_API_KEY=your-key
   TAVUS_REPLICA_ID=your-replica-id
   ```

### Beyond Presence

To integrate with Beyond Presence:

1. Get your Beyond Presence API key and avatar ID
2. Update `_generate_beyond_presence_frames()` in `avatar_video.py`
3. Set environment variables:
   ```env
   ENABLE_AVATAR_VIDEO=true
   AVATAR_PROVIDER=beyond-presence
   BEYOND_PRESENCE_API_KEY=your-key
   BEYOND_PRESENCE_AVATAR_ID=your-avatar-id
   ```

## Testing

1. **Enable avatar video**:
   ```env
   ENABLE_AVATAR_VIDEO=true
   AVATAR_PROVIDER=placeholder
   ```

2. **Start backend agent**:
   ```bash
   cd backend
   ./venv/bin/python -m livekit.agents dev agent.py
   ```

3. **Check logs** for:
   ```
   ✅ Published avatar video track (1280x720 @ 30fps)
   Generating placeholder avatar video frames
   ```

4. **Start frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

5. **Connect to agent** - video should appear automatically

6. **Check browser console** for:
   ```
   Video track received from agent
   Avatar video started
   ```

## Troubleshooting

### No Video in Frontend

1. **Check backend logs** - should see "Published avatar video track"
2. **Check frontend console** - should see "Video track received"
3. **Verify environment variables**:
   - Backend: `ENABLE_AVATAR_VIDEO=true`
   - Frontend: `VITE_AVATAR_PROVIDER=livekit-video`

### Video Not Publishing

1. **Check for errors** in backend logs
2. **Verify LiveKit connection** - agent must be connected to room
3. **Check video source creation** - ensure width/height are valid

### Video Stuttering

1. **Reduce frame rate**: `AVATAR_VIDEO_FPS=15`
2. **Reduce resolution**: `AVATAR_VIDEO_WIDTH=640` `AVATAR_VIDEO_HEIGHT=360`
3. **Check network quality** - video requires stable connection

## Implementation Notes

- Video frames are generated in a background task
- Frame generation runs continuously while agent is active
- Placeholder generates animated gradient pattern
- Real avatar services should sync frames with audio output
- Video track is published immediately, frames stream continuously

## Next Steps

1. **Test with placeholder** to verify video track publishing works
2. **Integrate Tavus or Beyond Presence** by updating frame generation functions
3. **Sync with audio** - ensure avatar lip movements match speech
4. **Optimize performance** - adjust resolution/fps based on network
