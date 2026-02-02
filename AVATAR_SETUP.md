# Quick Avatar Setup Guide

## Quick Start

1. **Set environment variables** in `frontend/.env`:
   ```env
   VITE_AVATAR_PROVIDER=livekit-video
   ```

2. **Start the frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

3. **Connect to the agent** - the avatar will automatically display if the agent publishes video tracks.

## Avatar Provider Options

### Option 1: LiveKit Video (Recommended for Real-time)

The agent publishes video tracks directly through LiveKit. This provides the smoothest experience.

**Setup:**
```env
VITE_AVATAR_PROVIDER=livekit-video
```

**Backend:** The agent can publish video tracks (see `backend/avatar_video.py` for implementation guide).

### Option 2: Tavus

Use Tavus API for avatar rendering.

**Setup:**
```env
VITE_AVATAR_PROVIDER=tavus
VITE_TAVUS_REPLICA_ID=your-replica-id
VITE_TAVUS_API_KEY=your-api-key
```

**Implementation:** Update `AvatarPlayer.tsx` with Tavus SDK integration (see `AVATAR_INTEGRATION.md`).

### Option 3: Beyond Presence

Use Beyond Presence API for avatar rendering.

**Setup:**
```env
VITE_AVATAR_PROVIDER=beyond-presence
VITE_BEYOND_PRESENCE_API_KEY=your-api-key
VITE_BEYOND_PRESENCE_AVATAR_ID=your-avatar-id
```

**Implementation:** Update `AvatarPlayer.tsx` with Beyond Presence SDK integration.

### Option 4: Placeholder (Default)

Simple placeholder avatar with speaking animations.

**Setup:**
```env
VITE_AVATAR_PROVIDER=none
```

## Features

✅ **Automatic video track detection** - Frontend automatically subscribes to video tracks from agent  
✅ **Speaking detection** - Avatar responds to agent speech with visual feedback  
✅ **Smooth video playback** - Optimized for continuous video streaming  
✅ **Multiple provider support** - Easy to switch between providers  
✅ **Graceful fallback** - Falls back to placeholder if video unavailable  

## Testing

1. Set `VITE_AVATAR_PROVIDER=livekit-video` in `.env`
2. Start frontend: `npm run dev`
3. Connect to agent
4. Check browser console for "Video track received from agent" message
5. Avatar should display automatically

## Troubleshooting

**No avatar showing:**
- Check console for video track messages
- Verify `VITE_AVATAR_PROVIDER` is set correctly
- Ensure agent is publishing video tracks (if using livekit-video)

**Avatar stuttering:**
- Check network connection quality
- Reduce video resolution in backend if publishing video

**Audio/video sync issues:**
- Ensure audio is playing correctly
- Check speaking detection is working (look for "Speaking..." status)

For detailed integration instructions, see `AVATAR_INTEGRATION.md`.
