# 🔧 Tool Call Data Channel Debugging

## Current Status

✅ **UI Component Works**: Test button successfully adds tool calls
✅ **React State Works**: State updates correctly
❌ **Data Channel Not Receiving**: No "📨 Data received" logs when tools are called

## Issue Analysis

The test button works, which means:
- ✅ `ToolCallDisplay` component works
- ✅ React state management works
- ✅ Component rendering works

But real tool calls from backend don't appear, which means:
- ❌ Data channel communication is failing
- OR backend is not sending data
- OR data is being sent but not received

## Debugging Steps

### Step 1: Check Backend Logs

When you trigger a tool call (say "I want to book an appointment"), check backend logs for:

```
🔧 TOOL CALL: identify_user
📤 Sending tool_call to frontend: identify_user
   Data: {"type":"tool_call","name":"identify_user",...}
   Room participants: 1
   📦 Data bytes length: 123
   📦 Data bytes preview: b'{"type":"tool_call"...'
   ✅ Data sent with topic 'tool_calls'
   ✅ Data also sent without topic (fallback)
```

**If you DON'T see these logs:**
- Tools are not being called
- Check if LLM is configured correctly
- Check if tools are registered with Agent

**If you see these logs but frontend doesn't receive:**
- Data channel issue
- Check LiveKit connection
- Check network/firewall

### Step 2: Check Frontend Console

When backend sends data, you should see:

```
📨 Data received: {kind: 1, topic: "tool_calls", ...}
📨 Full payload string: {"type":"tool_call","name":"identify_user",...}
📦 Parsed data: {type: "tool_call", ...}
   Type: tool_call
   Has type property: true
   Type value: tool_call
   Type === "tool_call": true
✅ MATCHED: data.type === "tool_call"
🔧 Tool call received: identify_user {...}
📋 Adding tool call: {name: "identify_user", ...}
📋 Updated tool calls - count: 1 calls: [...]
🔄 App: toolCalls state changed: 1 [...]
🔧 ToolCallDisplay: toolCalls updated: 1 [...]
```

**If you DON'T see "📨 Data received":**
- Data channel not working
- Check LiveKit connection
- Check if room is connected
- Check network tab for WebSocket

**If you see "📨 Data received" but no "📦 Parsed data":**
- JSON parsing issue
- Check payload string in log
- Check for encoding issues

### Step 3: Verify Data Channel Setup

The data channel listener is set up in `App.tsx`:

```typescript
newRoom.on(RoomEvent.DataReceived, (payload, participant, kind, topic) => {
  // ... handle data
})
```

**Important**: This listener is set up BEFORE `await newRoom.connect()`, which is correct.

### Step 4: Test Data Channel Manually

To test if data channel works at all, you can:

1. **Check backend logs** when you speak:
   - Do you see "🔧 TOOL CALL"?
   - Do you see "📤 Sending tool_call"?
   - Do you see "✅ Data sent"?

2. **Check frontend console**:
   - Do you see ANY "📨 Data received" logs?
   - Even for other data types?

3. **Check network tab**:
   - Is WebSocket connection active?
   - Are there any errors?

## Common Issues

### Issue 1: Backend Not Sending
**Symptoms**: No "🔧 TOOL CALL" in backend logs
**Causes**:
- Tools not being called by LLM
- LLM not configured for tool calling
- Tools not registered with Agent

**Fix**: 
- Check LLM configuration
- Verify tools are passed to Agent
- Try more explicit requests: "Use the identify_user tool"

### Issue 2: Data Channel Not Working
**Symptoms**: Backend sends but frontend doesn't receive
**Causes**:
- LiveKit connection issue
- Data channel not initialized
- Network/firewall blocking

**Fix**:
- Check LiveKit connection status
- Verify room is connected
- Check network tab for WebSocket errors
- Restart backend and frontend

### Issue 3: Topic Filtering
**Symptoms**: Data sent with topic but not received
**Causes**:
- Frontend filtering by topic
- Topic mismatch

**Fix**: 
- Frontend already accepts all topics (no filtering)
- Backend sends with and without topic (fallback)

### Issue 4: Encoding Issues
**Symptoms**: Data received but parsing fails
**Causes**:
- Wrong encoding
- Invalid JSON

**Fix**:
- Check payload string in console
- Verify JSON is valid
- Check encoding (should be UTF-8)

## Next Steps

1. **Trigger a tool call** (say "I want to book an appointment")
2. **Check backend logs** for "🔧 TOOL CALL" and "📤 Sending"
3. **Check frontend console** for "📨 Data received"
4. **Share the logs** so we can identify the exact issue

The enhanced logging will show exactly where the communication is failing!
