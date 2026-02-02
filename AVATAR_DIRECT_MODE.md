# Avatar Direct Mode - 2 Participants Only

## Overview

By default, Beyond Presence/Tavus create a **separate participant** (3 participants total). If you want video rendering on the **agent only** (2 participants), use **Direct Mode**.

## Configuration

### Direct Mode (2 Participants)

In `backend/.env`:
```env
AVATAR_MODE=direct
AVATAR_PROVIDER=beyond-presence  # or 'tavus' or 'placeholder'
ENABLE_AVATAR_VIDEO=true

# Beyond Presence credentials (if using beyond-presence)
BEY_API_KEY=your-api-key
BEY_AVATAR_ID=your-avatar-id
```

**Result**: 
- ✅ User participant
- ✅ Agent participant (publishes video directly)
- ❌ No separate avatar participant

### Separate Participant Mode (3 Participants) - Default

In `backend/.env`:
```env
AVATAR_MODE=separate  # or omit this line (default)
AVATAR_PROVIDER=beyond-presence

# Beyond Presence credentials
BEY_API_KEY=your-api-key
BEY_AVATAR_ID=your-avatar-id
```

**Result**:
- ✅ User participant
- ✅ Agent participant
- ✅ Avatar participant (separate)

## How Direct Mode Works

1. **Agent connects** to Beyond Presence/Tavus API
2. **Agent streams video frames** from the API
3. **Agent publishes video tracks** directly to LiveKit room
4. **Frontend displays** video from the agent participant

## Comparison

| Mode | Participants | Video Source | Use Case |
|------|-------------|--------------|----------|
| **Direct** | 2 (user + agent) | Agent publishes directly | Simpler setup, agent handles everything |
| **Separate** | 3 (user + agent + avatar) | Avatar participant publishes | Better for production, automatic lip-sync |

## Implementation Status

### ✅ Placeholder Video
- Works in direct mode
- Agent publishes test pattern video

### 🚧 Beyond Presence Direct Mode
- Currently uses placeholder video
- To implement: Stream video frames from Beyond Presence API to agent
- See `backend/avatar_video.py` → `_generate_beyond_presence_frames()`

### 🚧 Tavus Direct Mode
- Currently uses placeholder video
- To implement: Stream video frames from Tavus API to agent
- See `backend/avatar_video.py` → `_generate_tavus_frames()`

## Quick Start

To use direct mode with placeholder video (2 participants):

```env
AVATAR_MODE=direct
AVATAR_PROVIDER=placeholder
ENABLE_AVATAR_VIDEO=true
```

Restart backend agent. You'll have 2 participants with video from the agent.

## Next Steps

To implement real Beyond Presence/Tavus in direct mode:

1. Update `_generate_beyond_presence_frames()` in `backend/avatar_video.py`
2. Connect to Beyond Presence streaming API
3. Receive video frames
4. Convert to LiveKit VideoFrame format
5. Send to `video_source.capture_frame()`

Same process for Tavus in `_generate_tavus_frames()`.
