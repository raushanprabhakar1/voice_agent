# Avatar Integration Guide

This guide explains how to integrate avatars (Tavus, Beyond Presence, or LiveKit Video) with the SuperBryn Voice Agent.

## Overview

The avatar system supports three modes:
1. **LiveKit Video**: Agent publishes video tracks directly (recommended for real-time)
2. **Tavus**: Uses Tavus API for avatar rendering
3. **Beyond Presence**: Uses Beyond Presence API for avatar rendering

## Configuration

### Environment Variables

Add these to your `frontend/.env` file:

```env
# Avatar Provider: 'livekit-video', 'tavus', 'beyond-presence', or 'none'
VITE_AVATAR_PROVIDER=livekit-video

# Tavus Configuration (if using Tavus)
VITE_TAVUS_REPLICA_ID=your-replica-id
VITE_TAVUS_API_KEY=your-tavus-api-key

# Beyond Presence Configuration (if using Beyond Presence)
VITE_BEYOND_PRESENCE_API_KEY=your-api-key
VITE_BEYOND_PRESENCE_AVATAR_ID=your-avatar-id
```

## Option 1: LiveKit Video (Recommended)

The agent can publish video tracks directly through LiveKit. This provides the smoothest real-time experience.

### Backend Setup

The backend agent can publish video tracks. To enable this, you would need to:

1. **Generate or stream video** from your avatar service
2. **Publish video tracks** to the LiveKit room

Example backend code (to add to `agent.py`):

```python
# In entrypoint function, after connecting to room
from livekit import rtc

# Create a video track source (this would come from your avatar service)
# For now, this is a placeholder - you'd integrate with Tavus/Beyond Presence API here
video_source = rtc.VideoSource(1920, 1080)  # Adjust resolution as needed
video_track = rtc.LocalVideoTrack.create_video_track("avatar-video", video_source)

# Publish the video track
await ctx.room.local_participant.publish_track(video_track)
```

### Frontend

The frontend automatically subscribes to video tracks when `VITE_AVATAR_PROVIDER=livekit-video` is set.

## Option 2: Tavus Integration

Tavus provides API-based avatar rendering. To integrate:

### 1. Install Tavus SDK (if available)

```bash
cd frontend
npm install @tavus/react  # or the appropriate Tavus package
```

### 2. Update AvatarPlayer Component

Replace the Tavus placeholder in `AvatarPlayer.tsx` with actual Tavus SDK integration:

```typescript
import { Tavus } from '@tavus/react'  // Adjust import based on actual SDK

// In AvatarPlayer component:
if (avatarProvider === 'tavus') {
  return (
    <div className="avatar-player-container">
      <Tavus
        replicaId={tavusReplicaId}
        apiKey={tavusApiKey}
        audioTrack={audioTrack}  // Sync with agent audio
        onReady={() => setAvatarReady(true)}
        onError={(err) => setError(err.message)}
      />
    </div>
  )
}
```

### 3. Sync with Audio

The avatar should automatically sync with the audio track from the agent. The `isSpeaking` state is passed to the component to trigger animations.

## Option 3: Beyond Presence Integration

Beyond Presence provides avatar rendering services. To integrate:

### 1. Install Beyond Presence SDK (if available)

```bash
cd frontend
npm install @beyondpresence/react  # or the appropriate package
```

### 2. Update AvatarPlayer Component

Replace the Beyond Presence placeholder with actual SDK integration:

```typescript
import { BeyondPresence } from '@beyondpresence/react'  // Adjust import

// In AvatarPlayer component:
if (avatarProvider === 'beyond-presence') {
  return (
    <div className="avatar-player-container">
      <BeyondPresence
        avatarId={beyondPresenceAvatarId}
        apiKey={beyondPresenceApiKey}
        audioTrack={audioTrack}
        onReady={() => setAvatarReady(true)}
      />
    </div>
  )
}
```

## Option 4: Backend Video Publishing (Advanced)

For the smoothest experience, you can have the backend agent publish video tracks directly:

### Backend Implementation

1. **Generate avatar video** from text/audio using Tavus/Beyond Presence API
2. **Stream video frames** to LiveKit as a video track
3. **Frontend automatically displays** the video track

Example backend code structure:

```python
# In agent.py, add video publishing capability
async def publish_avatar_video(ctx: JobContext, audio_stream):
    """Publish avatar video track synchronized with audio"""
    from livekit import rtc
    
    # Create video source
    video_source = rtc.VideoSource(1280, 720)
    video_track = rtc.LocalVideoTrack.create_video_track("avatar", video_source)
    
    # Publish track
    await ctx.room.local_participant.publish_track(video_track)
    
    # Stream video frames (this would integrate with Tavus/Beyond Presence)
    # For each audio chunk, generate corresponding video frame
    async for audio_chunk in audio_stream:
        # Call Tavus/Beyond Presence API to get video frame
        video_frame = await generate_avatar_frame(audio_chunk)
        await video_source.capture_frame(video_frame)
```

## Current Implementation

The current implementation:

1. ✅ **Detects video tracks** from the agent automatically
2. ✅ **Displays video** when available
3. ✅ **Syncs with speaking state** for visual feedback
4. ✅ **Supports multiple providers** via configuration
5. ✅ **Falls back gracefully** if video is not available

## Testing

1. **Set avatar provider** in `.env`:
   ```env
   VITE_AVATAR_PROVIDER=livekit-video
   ```

2. **Start the frontend**:
   ```bash
   npm run dev
   ```

3. **Connect to the agent** - if the agent publishes video tracks, they will automatically display

4. **Check browser console** for video track subscription logs

## Troubleshooting

### No Video Appearing

1. **Check if agent publishes video**: Look for "Video track received from agent" in console
2. **Verify provider setting**: Ensure `VITE_AVATAR_PROVIDER` is set correctly
3. **Check browser permissions**: Video may require additional permissions
4. **Network issues**: Video tracks require stable connection

### Video Stuttering

1. **Check network quality**: Use LiveKit's connection quality indicators
2. **Reduce video resolution**: Lower resolution in backend video source
3. **Check frame rate**: Ensure consistent frame rate (e.g., 30fps)

### Audio/Video Sync Issues

1. **Ensure audio track is attached**: Check that audio is playing
2. **Check speaking detection**: Verify `isSpeaking` state changes correctly
3. **Provider-specific sync**: Tavus/Beyond Presence should handle sync automatically

## Next Steps

1. **Choose your avatar provider** (Tavus, Beyond Presence, or LiveKit Video)
2. **Set up API keys** and get replica/avatar IDs
3. **Configure environment variables** in `frontend/.env`
4. **Test the integration** with a voice call
5. **Customize styling** in `AvatarPlayer.css` if needed

## Resources

- [Tavus Documentation](https://docs.tavus.io/)
- [Beyond Presence Documentation](https://docs.beyondpresence.com/)
- [LiveKit Video Tracks](https://docs.livekit.io/client-sdk-js/tracks/)
