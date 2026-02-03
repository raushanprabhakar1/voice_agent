# 🔧 Fix: Agent Chat Not Working in Vercel (But Works Locally)

## The Problem

The voice agent chat works fine in localhost but not in Vercel - no agent responds when users connect.

## Root Cause

The Vercel serverless function (`api/token.js`) was **missing the agent dispatch logic** that explicitly tells LiveKit to send the agent to the room. The local `server.js` had this logic, but it wasn't in the production function.

## What Was Fixed

✅ **Added agent dispatch logic to `frontend/api/token.js`**:
- Creates/ensures the room exists
- Explicitly dispatches the agent named "voice-agent" to the room
- This matches the backend agent configuration (agent name: "voice-agent")

## Required Environment Variables in Vercel

Make sure these are set in **Vercel → Settings → Environment Variables**:

### For the Token API (Serverless Function):
- `LIVEKIT_API_KEY` - Your LiveKit API key
- `LIVEKIT_API_SECRET` - Your LiveKit API secret  
- `LIVEKIT_URL` - Your LiveKit server URL (e.g., `wss://your-project.livekit.cloud`)

### For the Frontend (Build-time):
- `VITE_LIVEKIT_URL` - Your LiveKit server URL (same as above)
  - **Important**: This must start with `wss://` not `https://`
  - Example: `wss://your-project.livekit.cloud`

**Critical**: Make sure these are set for **Production** environment (and Preview if needed).

## Backend Agent Must Be Running

The backend agent (deployed on Railway or elsewhere) must be:
1. ✅ Running and connected to LiveKit
2. ✅ Registered with agent name: `"voice-agent"` (this matches the dispatch call)
3. ✅ Listening for jobs from LiveKit

## How It Works Now

1. **User clicks "Start Voice Call"** in the frontend
2. **Frontend calls `/api/token`** (Vercel serverless function)
3. **Token function**:
   - Generates LiveKit access token
   - Creates/ensures the room exists
   - **Explicitly dispatches agent "voice-agent" to the room** ← This was missing!
4. **Backend agent receives dispatch** and connects to the room
5. **User and agent can now chat**

## Verify It's Working

1. **Check Vercel Function Logs**:
   - Go to Deployments → Latest → Functions → `/api/token`
   - Look for: `✅ Agent dispatched to room: voice-agent-room`
   - Should see: `Dispatch ID: ...` and `Agent name: voice-agent`

2. **Check Backend Logs** (Railway or wherever backend is deployed):
   - Should see: `📥 JOB REQUEST RECEIVED!`
   - Should see: `✅ Job accepted - entrypoint will be called`
   - Should see: `🚀 AGENT ENTRYPOINT CALLED!`

3. **Test in Browser**:
   - Open browser console (F12)
   - Click "Start Voice Call"
   - Should see connection messages
   - Agent should respond when you speak

## Troubleshooting

### Agent Still Not Responding?

1. **Check Backend is Running**:
   - Verify backend agent is deployed and running
   - Check backend logs for connection errors
   - Make sure backend has same LiveKit credentials

2. **Check Agent Name Matches**:
   - Backend agent name must be: `"voice-agent"` (in `backend/agent.py` line 900)
   - Token function dispatches: `"voice-agent"` (in `frontend/api/token.js` line 105)
   - These must match exactly!

3. **Check Environment Variables**:
   - All three `LIVEKIT_*` variables set in Vercel
   - `VITE_LIVEKIT_URL` set in Vercel
   - Variables set for Production environment
   - Redeployed after setting variables

4. **Check Function Logs**:
   - Look for dispatch errors in Vercel function logs
   - Look for room creation errors
   - Check if agent dispatch succeeded

5. **Check Browser Console**:
   - Look for connection errors
   - Check if token was received
   - Check if room connection succeeded

## Common Issues

### "Agent dispatched" but no response
- **Cause**: Backend agent not running or not connected to LiveKit
- **Fix**: Check backend deployment and logs

### "Failed to dispatch agent" error
- **Cause**: Agent name mismatch or backend not registered
- **Fix**: Verify agent name is exactly `"voice-agent"` in both places

### Room connects but agent never joins
- **Cause**: Backend agent not listening or dispatch failed silently
- **Fix**: Check backend logs for job requests

## Summary

The fix adds explicit agent dispatch to the token API, which tells LiveKit to send the agent to the room when a user connects. This is required for LiveKit Cloud's explicit dispatch model.

After deploying this fix and ensuring all environment variables are set, the agent should respond in production just like it does locally.
