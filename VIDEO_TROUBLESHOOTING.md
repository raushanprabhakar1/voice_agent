# Video Rendering Troubleshooting Guide

## Quick Checks

1. **Backend Environment Variables**:
   ```env
   ENABLE_AVATAR_VIDEO=true
   AVATAR_PROVIDER=placeholder
   ```

2. **Frontend Environment Variables**:
   ```env
   VITE_AVATAR_PROVIDER=livekit-video
   ```

3. **Check Backend Logs** for:
   - `✅ Published avatar video track`
   - `Generating placeholder avatar video frames`
   - `Captured frame X` (every 2 seconds)

4. **Check Frontend Console** for:
   - `Video track received from agent`
   - `Video track published, subscribing...`
   - `AvatarPlayer: Attaching video track to element`
   - `AvatarPlayer: Video track attached successfully`

## Common Issues

### Issue 1: No Video Track Published

**Symptoms**: Backend logs show "Avatar video disabled" or no video track message

**Solution**:
- Set `ENABLE_AVATAR_VIDEO=true` in backend `.env`
- Restart backend agent
- Check logs for "Published avatar video track"

### Issue 2: Video Track Not Subscribed

**Symptoms**: Frontend console shows "Video track received" but no video displays

**Solution**:
- Check browser console for subscription errors
- Verify `VITE_AVATAR_PROVIDER=livekit-video` in frontend `.env`
- Check network tab for WebRTC connection issues

### Issue 3: Video Element Not Attaching

**Symptoms**: Console shows "Video track received" but "AvatarPlayer: Video element not available"

**Solution**:
- Check that `AvatarPlayer` component is rendered
- Verify video element ref is set correctly
- Check for React rendering errors

### Issue 4: Video Frames Not Generating

**Symptoms**: Video track published but no frames appear

**Solution**:
- Check backend logs for frame generation errors
- Verify numpy is installed: `pip install numpy`
- Check for errors in `_generate_placeholder_frames`

### Issue 5: Video Black Screen

**Symptoms**: Video element shows but is black

**Solution**:
- Check that frames are being captured (look for "Captured frame" logs)
- Verify VideoFrame format is correct (RGBA)
- Check browser console for video playback errors

## Debugging Steps

1. **Enable verbose logging**:
   - Backend: Already logs frame generation
   - Frontend: Check browser console for all video-related messages

2. **Check video track state**:
   ```javascript
   // In browser console
   // Find the video track
   const track = room.remoteParticipants.values().next().value.trackPublications.values().next().value.track
   console.log('Track:', track)
   console.log('Kind:', track.kind)
   console.log('SID:', track.sid)
   console.log('Muted:', track.isMuted)
   ```

3. **Check video element**:
   ```javascript
   // In browser console
   const video = document.querySelector('.avatar-video')
   console.log('Video element:', video)
   console.log('Video src:', video?.srcObject)
   console.log('Video readyState:', video?.readyState)
   ```

4. **Check frame generation**:
   - Look for "Captured frame" messages in backend logs
   - Should see messages every 2 seconds if frames are generating

## Testing Checklist

- [ ] Backend: `ENABLE_AVATAR_VIDEO=true` set
- [ ] Backend: Logs show "Published avatar video track"
- [ ] Backend: Logs show "Generating placeholder avatar video frames"
- [ ] Backend: Logs show "Captured frame" messages
- [ ] Frontend: `VITE_AVATAR_PROVIDER=livekit-video` set
- [ ] Frontend: Console shows "Video track received from agent"
- [ ] Frontend: Console shows "Video track published, subscribing..."
- [ ] Frontend: Console shows "AvatarPlayer: Attaching video track"
- [ ] Frontend: Console shows "AvatarPlayer: Video track attached successfully"
- [ ] Browser: Video element is visible and playing

## Still Not Working?

1. **Check LiveKit connection**:
   - Verify agent is connected to room
   - Check LiveKit server logs
   - Verify network connectivity

2. **Check browser compatibility**:
   - Use Chrome or Firefox (latest versions)
   - Check browser console for WebRTC errors
   - Verify WebRTC is enabled in browser

3. **Check video codec support**:
   - LiveKit should handle codec negotiation automatically
   - Check browser console for codec errors

4. **Try reducing resolution**:
   ```env
   AVATAR_VIDEO_WIDTH=640
   AVATAR_VIDEO_HEIGHT=360
   AVATAR_VIDEO_FPS=15
   ```

5. **Check for errors in all logs**:
   - Backend agent logs
   - Frontend browser console
   - LiveKit server logs (if accessible)
