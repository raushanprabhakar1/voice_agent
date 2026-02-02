# How to Have Only 2 Participants (User + Agent)

## Current Setup (3 Participants)

When using Beyond Presence, you have:
1. **User** - The person using the web app
2. **Main Agent** - Your voice agent
3. **Beyond Presence Avatar** - Separate participant for video

## Why 3 Participants?

Beyond Presence requires the avatar to be a **separate participant** because:
- It handles video rendering on their servers
- It needs to publish video tracks independently
- It receives audio from the agent for lip-sync

## Solution: Use Placeholder Video (2 Participants)

To have only **2 participants** (user + agent), use placeholder video instead:

### Option 1: Disable Beyond Presence, Use Placeholder

In `backend/.env`:
```env
# Don't use Beyond Presence
# AVATAR_PROVIDER=placeholder  # or remove this line

# Enable placeholder video
ENABLE_AVATAR_VIDEO=true
AVATAR_PROVIDER=placeholder
```

This gives you:
- ✅ User participant
- ✅ Main agent participant (publishes video directly)
- ❌ No separate avatar participant

### Option 2: Keep Beyond Presence but Use Fallback

If Beyond Presence fails (concurrency limit), the system automatically falls back to placeholder video, giving you 2 participants.

## Comparison

| Setup | Participants | Video Source |
|-------|-------------|--------------|
| **Beyond Presence** | 3 (user + agent + avatar) | Beyond Presence servers |
| **Placeholder Video** | 2 (user + agent) | Local agent (test pattern) |
| **No Video** | 2 (user + agent) | None |

## Recommendation

- **For production**: Use Beyond Presence (3 participants) - better quality, lip-sync
- **For testing/development**: Use placeholder (2 participants) - simpler, no API limits

## To Switch

1. **To 2 participants**: Set `AVATAR_PROVIDER=placeholder` and `ENABLE_AVATAR_VIDEO=true`
2. **To 3 participants**: Set `AVATAR_PROVIDER=beyond-presence` with API keys

Restart backend after changing `.env`.
