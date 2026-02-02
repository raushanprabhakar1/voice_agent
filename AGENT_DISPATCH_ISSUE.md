# Agent Dispatch Issue - LiveKit Cloud

## Current Status
- ✅ Agent worker is running and registered (`registered_workers` appears in logs)
- ✅ Agent name is set correctly (`voice-agent` or empty for auto-dispatch)
- ❌ Job requests are NOT being received when participants join
- ❌ Entrypoint is NOT being called

## The Problem
LiveKit Cloud requires **explicit agent dispatch**. The agent worker is registered, but LiveKit isn't automatically assigning it to rooms when participants join.

## Solutions to Try

### Option 1: Use LiveKit Cloud Dashboard
1. Go to your LiveKit Cloud dashboard
2. Check if there's a setting for "Auto-dispatch agents" or "Agent assignment"
3. Enable it if available

### Option 2: Use Webhooks (Recommended)
LiveKit Cloud supports webhooks that trigger when participants join. You can:
1. Set up a webhook endpoint in your backend
2. Configure it in LiveKit Cloud dashboard to call your endpoint when `participant_joined` event occurs
3. In the webhook handler, use the AgentDispatch API to explicitly dispatch the agent

### Option 3: Check Agent Name Match
Make sure:
- Backend agent name matches exactly what's expected
- Try both `agent_name=""` (auto-dispatch) and `agent_name="voice-agent"` (explicit)
- Restart the agent after changing the name

### Option 4: Verify Room Creation
The room must exist BEFORE participants join. Make sure:
- Room is created via `RoomServiceClient.createRoom()` before generating tokens
- Room creation succeeds (check for errors in token server logs)

## Next Steps
1. Check LiveKit Cloud dashboard for agent/webhook settings
2. Try setting up a webhook endpoint
3. Verify the agent worker is in the same region as your LiveKit Cloud instance
4. Contact LiveKit support if the issue persists

## Debugging Commands
```bash
# Check if agent is registered
# Look for "registered_workers" in backend logs

# Check if room exists
# Look for "Room ready" in token server logs

# Check for job requests
# Look for "📥 JOB REQUEST RECEIVED!" in backend logs
```
