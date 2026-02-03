# Architecture: How Frontend and Backend Connect

## Overview

The frontend and backend **do NOT directly connect to each other**. Instead, they both connect to **LiveKit Server**, which acts as the intermediary.

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Frontend   │────────▶│  LiveKit     │◀────────│   Backend   │
│  (Vercel)   │         │   Server     │         │  (Railway)  │
│             │         │              │         │             │
│ React App   │         │  Manages     │         │  Python     │
│             │         │  Rooms &     │         │  Agent      │
│             │         │  Routes      │         │             │
│             │         │  Media       │         │             │
└─────────────┘         └──────────────┘         └─────────────┘
      │                        │                        │
      │                        │                        │
      └────────────────────────┴────────────────────────┘
                    All connect to same
                    LiveKit Server URL
```

## Connection Flow

### Step 1: Frontend Gets Token
- Frontend calls `/api/token` (Vercel serverless function)
- Token API generates a LiveKit access token
- Returns token + LiveKit URL to frontend

### Step 2: Frontend Connects to LiveKit
- Frontend uses token to connect to LiveKit server
- Joins room: `voice-agent-room`
- Starts publishing audio (microphone)

### Step 3: LiveKit Dispatches Agent
- When frontend joins the room, LiveKit detects it
- LiveKit automatically dispatches the backend agent to the same room
- Backend agent receives a "job request" for that room

### Step 4: Backend Agent Joins Room
- Backend agent accepts the job
- Connects to the same LiveKit room (`voice-agent-room`)
- Now both frontend and backend are in the same room

### Step 5: Communication
- **Audio**: Frontend sends audio → LiveKit → Backend agent
- **Audio**: Backend agent sends audio → LiveKit → Frontend
- **Video**: Backend agent sends video → LiveKit → Frontend
- **Data**: Backend agent sends tool calls → LiveKit → Frontend

## Key Points

1. **No Direct Connection**: Frontend and backend never talk directly
2. **LiveKit is the Hub**: All communication goes through LiveKit
3. **Same Server URL**: Both use the same `LIVEKIT_URL`
4. **Same Room Name**: Both join `voice-agent-room`
5. **Token API is Just for Auth**: The `/api/token` endpoint only generates tokens, it doesn't connect them

## Configuration

### Frontend (Vercel)
```env
VITE_LIVEKIT_URL=wss://your-livekit-server.com  # For frontend
LIVEKIT_URL=wss://your-livekit-server.com       # For token API
LIVEKIT_API_KEY=your-key                        # For token API
LIVEKIT_API_SECRET=your-secret                 # For token API
```

### Backend (Railway)
```env
LIVEKIT_URL=wss://your-livekit-server.com      # Same URL!
LIVEKIT_API_KEY=your-key                       # Same key!
LIVEKIT_API_SECRET=your-secret                # Same secret!
```

**Important**: They use the **same LiveKit server URL, API key, and secret**!

## Room Flow

1. **User clicks "Start Voice Call"**
   - Frontend gets token from `/api/token`
   - Frontend connects to LiveKit: `wss://your-livekit-server.com`
   - Frontend joins room: `voice-agent-room`

2. **LiveKit detects user joined**
   - LiveKit sees a participant in `voice-agent-room`
   - LiveKit dispatches agent named `voice-agent` to that room

3. **Backend agent receives job**
   - `job_request_handler` is called
   - Agent accepts the job
   - Agent connects to same LiveKit server
   - Agent joins same room: `voice-agent-room`

4. **Now they're connected!**
   - Both in same room
   - Can exchange audio/video/data
   - Communication happens through LiveKit

## Token API Purpose

The `/api/token` endpoint is **NOT** the connection between frontend and backend.

It's only used to:
- Generate LiveKit access tokens (for authentication)
- Return the LiveKit server URL

The actual connection happens when:
- Frontend connects to LiveKit using the token
- Backend agent is dispatched by LiveKit to the same room

## Verification

To verify they're connected:

1. **Check frontend console**: Should see "Room connected successfully"
2. **Check frontend console**: Should see "Remote participant" (the agent)
3. **Check backend logs**: Should see "JOB REQUEST RECEIVED"
4. **Check backend logs**: Should see "AGENT ENTRYPOINT CALLED"
5. **Check backend logs**: Should see "Connected to room: voice-agent-room"

If you see these, they're connected through LiveKit!
