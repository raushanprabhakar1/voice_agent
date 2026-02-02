# Fix: Avatar Video Not Displaying

## Issue
When using Tavus or Beyond Presence, the avatar placeholder is shown instead of the actual video.

## Root Cause
Tavus and Beyond Presence avatars join the LiveKit room as **separate participants** (not the agent participant). The frontend was only looking for video tracks from the agent participant.

## Solution Applied

### 1. Updated `VoiceAgent.tsx`
- Now searches for video tracks from **ALL remote participants**
- Subscribes to video tracks when new participants join (avatar might join after agent)
- Logs participant identities for debugging

### 2. Updated `AvatarPlayer.tsx`
- Changed logic to use video tracks for Tavus/Beyond Presence (they publish through LiveKit)
- Shows placeholder only when video track is not available yet
- Displays "Waiting for video..." message while loading

## How It Works Now

1. **Backend**: Beyond Presence/Tavus avatar joins as separate participant
2. **Backend**: Avatar publishes video and audio tracks
3. **Frontend**: Detects video track from any participant
4. **Frontend**: Subscribes to and displays the video track
5. **Frontend**: Shows placeholder only if video track not found

## Testing

1. **Check backend logs** for:
   ```
   ✅ Beyond Presence avatar session started successfully
   Avatar will handle audio/video publishing
   ```

2. **Check frontend console** for:
   ```
   Participant connected: [avatar-identity]
   Video track published from [avatar-identity], subscribing...
   Video track received from [avatar-identity]
   ```

3. **If still showing placeholder**:
   - Check that `AVATAR_PROVIDER=beyond-presence` in backend `.env`
   - Check that Beyond Presence plugin is installed: `pip install 'livekit-agents[bey]'`
   - Check that `BEY_API_KEY` and `BEY_AVATAR_ID` are set correctly
   - Restart backend agent after changing `.env`

## Expected Behavior

- **Before**: Placeholder with "Beyond Presence Avatar" text
- **After**: Actual video stream from Beyond Presence avatar

The video should appear automatically once the avatar participant joins and publishes its video track.
