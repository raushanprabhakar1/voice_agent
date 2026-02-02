# Debugging Guide - Agent Not Responding

## Quick Debug Steps

### 1. Verify All Services Are Running

```bash
# Terminal 1: Backend Agent
cd backend
python agent.py dev

# Terminal 2: Token Server  
cd frontend
npm run dev:token

# Terminal 3: Frontend
cd frontend
npm run dev
```

### 2. Check Backend Logs

Look for these in the backend terminal:
- ✅ "Agent connected" or "Connected to room"
- ✅ "User speech: ..." (when you speak)
- ✅ "LLM response generated"
- ✅ "TTS synthesis started"
- ❌ Any ERROR messages

### 3. Check Frontend Console

Open browser DevTools (F12) and check:
- ✅ "Room connected"
- ✅ "Track subscribed: audio"
- ❌ Any red error messages

### 4. Test Microphone

1. Click "Start Voice Call"
2. Browser should ask for microphone permission - **ALLOW IT**
3. Check if microphone icon shows as active
4. Speak and watch backend logs for transcription

### 5. Common Issues

#### Issue: No transcription in backend
**Fix:** 
- Check microphone permissions in browser
- Verify Deepgram API key in `.env`
- Check if audio track is being published (frontend console)

#### Issue: LLM not responding
**Fix:**
- Verify LLM API key in `.env`
- Check LLM provider setting (openai/azure/anthropic/etc)
- Look for LLM errors in backend logs

#### Issue: No audio output
**Fix:**
- Check Cartesia API key in `.env`
- Verify audio element is attached (frontend)
- Check browser volume is not muted
- Look for TTS errors in backend logs

#### Issue: Tool calls not working
**Fix:**
- Check if tools are registered (backend logs should show tool definitions)
- Verify tool execution doesn't throw errors
- Check tool results are being sent back to LLM

## Adding Debug Logging

Add this to `backend/agent.py` at the top:

```python
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
```

This will show detailed logs of what's happening.

## Test Commands

### Test 1: Basic Connection
1. Start all services
2. Open frontend
3. Click "Start Voice Call"
4. **Expected:** Should connect without errors

### Test 2: Audio Input
1. After connecting, speak: "Hello"
2. **Expected:** Backend should log transcription

### Test 3: Agent Response
1. After speaking, wait 2-3 seconds
2. **Expected:** Should hear agent response

### Test 4: Tool Call
1. Say: "I want to book an appointment"
2. **Expected:** 
   - Tool call appears in UI
   - Agent asks for phone number
   - Agent responds with voice

## Still Not Working?

Share:
1. Backend logs (last 50 lines)
2. Frontend console errors
3. What you see vs. what you expect
4. Which step fails (connection, transcription, response, etc.)
