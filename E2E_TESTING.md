# End-to-End Testing Guide

This guide will help you test the voice agent end-to-end and debug response issues.

## Prerequisites

1. **Backend agent running**: `python agent.py dev`
2. **Token server running**: `npm run dev:token` (in frontend directory)
3. **Frontend running**: `npm run dev` (in frontend directory)
4. **All API keys configured** in `.env` files

## Testing Steps

### 1. Check Agent is Running

In the backend terminal, you should see:
```
INFO ... Agent started
INFO ... Connected to room
```

### 2. Check Frontend Connection

1. Open browser console (F12)
2. Click "Start Voice Call"
3. Check for errors in console
4. Verify you see: "Connected to room"

### 3. Test Audio Input

1. **Check microphone permissions**: Browser should ask for mic access
2. **Verify audio is being sent**: 
   - Look for "Listening..." status in UI
   - Check browser console for audio track events
   - In backend logs, you should see transcription events

### 4. Test Basic Conversation

Say: **"Hello, I'd like to book an appointment"**

**Expected behavior:**
- Backend should transcribe your speech
- Agent should respond with voice
- You should hear the response
- UI should show "Speaking..." when agent talks

### 5. Test Tool Calls

Say: **"I want to book an appointment for tomorrow at 2 PM"**

**Expected behavior:**
- Agent should ask for your phone number first
- Tool call should appear in UI (ToolCallDisplay component)
- Agent should confirm the booking

### 6. Debug Checklist

If you're not receiving responses:

#### Backend Issues:
- [ ] Check agent logs for errors
- [ ] Verify LLM API key is correct
- [ ] Check Deepgram API key (for STT)
- [ ] Check Cartesia API key (for TTS)
- [ ] Verify tools are registered (check logs)

#### Frontend Issues:
- [ ] Check browser console for errors
- [ ] Verify microphone is enabled
- [ ] Check if audio tracks are being received
- [ ] Verify token server is running on port 3001
- [ ] Check network tab for failed requests

#### Connection Issues:
- [ ] Verify LiveKit URL is correct
- [ ] Check LiveKit API keys
- [ ] Ensure room connection is successful
- [ ] Verify both frontend and agent are in same room

## Common Issues & Fixes

### Issue: "No response from agent"

**Possible causes:**
1. Agent not receiving audio
   - Check microphone permissions
   - Verify audio track is being published
   - Check backend logs for transcription events

2. LLM not responding
   - Verify LLM API key
   - Check LLM provider is correct
   - Look for LLM errors in backend logs

3. TTS not working
   - Verify Cartesia API key
   - Check TTS errors in backend logs

### Issue: "Tool calls not executing"

**Check:**
- Tools are registered with LLM (check logs)
- Tool call handler is being called
- Tool execution is successful (check logs)

### Issue: "Audio not playing"

**Check:**
- Browser audio permissions
- Audio element is attached to track
- Remote audio track is subscribed
- Browser volume is not muted

## Debug Commands

### Backend Logging

Add debug prints to see what's happening:

```python
# In agent.py, add logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Frontend Console

Check browser console for:
- Room connection events
- Track subscription events
- Data channel messages
- Errors

### Network Tab

Check browser Network tab for:
- Token API call (should return 200)
- WebSocket connection to LiveKit
- Any failed requests

## Manual Testing Script

1. **Start all services:**
   ```bash
   # Terminal 1: Backend
   cd backend
   python agent.py dev
   
   # Terminal 2: Token server
   cd frontend
   npm run dev:token
   
   # Terminal 3: Frontend
   cd frontend
   npm run dev
   ```

2. **Open browser to http://localhost:3000**

3. **Test flow:**
   - Click "Start Voice Call"
   - Allow microphone access
   - Say: "Hello"
   - Wait for response
   - Say: "I want to book an appointment"
   - Follow agent prompts

## Expected Logs

### Backend (Agent):
```
INFO ... Agent connected
INFO ... User speech: "hello"
INFO ... LLM response generated
INFO ... TTS synthesis started
INFO ... Tool call: identify_user
INFO ... Tool result: {"success": true, ...}
```

### Frontend Console:
```
Room connected
Track subscribed: audio
Data received: {"type": "tool_call", ...}
```

## Next Steps

If issues persist:
1. Share backend logs
2. Share frontend console errors
3. Share network tab errors
4. Describe what you see vs. what you expect
