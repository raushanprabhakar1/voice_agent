# 🔧 Tool Call Debugging - Step by Step

## Current Issue
Tool calls are not visible in the UI. The component shows "0 calls" even when tools are executed.

## Quick Test

I've added a **"🧪 Test UI"** button. Click it to verify:
1. ✅ UI component works (if test call appears, UI is fine)
2. ✅ State updates work (if test call appears, React state is fine)
3. ❌ Data channel issue (if test works but real calls don't, it's a data channel problem)

## Step-by-Step Debugging

### Step 1: Test the UI Component

1. **Start the voice call**
2. **Click "🧪 Test UI (Add Test Tool Call)" button**
3. **Check if a tool call appears**

**If test call appears:**
- ✅ UI component works
- ✅ React state works
- ❌ Problem is data channel communication
- → Go to Step 2

**If test call doesn't appear:**
- ❌ UI component issue
- → Check browser console for React errors
- → Check if component is rendering

### Step 2: Check if Tools Are Being Called

**In Backend Logs**, look for:
```
🔧 TOOL CALL: identify_user
📤 Sending tool_call to frontend: identify_user
   Data: {"type":"tool_call","name":"identify_user",...}
   Room participants: 1
   ✅ Data sent with topic 'tool_calls'
```

**If you see this:**
- ✅ Tools are being called
- ✅ Backend is trying to send
- → Go to Step 3

**If you DON'T see this:**
- ❌ Tools are not being called
- → Try saying: "I want to book an appointment"
- → Check if LLM is configured correctly
- → Check if tools are registered with LLM

### Step 3: Check if Data is Being Received

**In Browser Console**, look for:
```
📨 Data received: {kind: 1, topic: "tool_calls", ...}
📦 Parsed data: {type: "tool_call", name: "identify_user", ...}
   Type: tool_call
🔧 Tool call received: identify_user {...}
📋 Updated tool calls: 1
```

**If you see "📨 Data received":**
- ✅ Data channel is working
- → Check if data.type === 'tool_call'
- → Check if parsing works

**If you DON'T see "📨 Data received":**
- ❌ Data channel not working
- → Check LiveKit connection
- → Check if room is connected
- → Check network tab for WebSocket

### Step 4: Check Data Format

**In Browser Console**, check the `payloadPreview`:
```
payloadPreview: '{"type":"tool_call","name":"identify_user",...}'
```

**If preview looks correct:**
- ✅ Data format is correct
- → Check JSON parsing

**If preview looks wrong:**
- ❌ Data format issue
- → Check backend JSON encoding
- → Check for encoding issues

## Common Issues & Fixes

### Issue 1: No "📨 Data received" in console
**Problem**: Data channel not working
**Possible Causes**:
- LiveKit connection not established
- Data channel not initialized
- Network/firewall blocking

**Fixes**:
1. Check LiveKit connection status
2. Verify room is connected
3. Check network tab for WebSocket connection
4. Restart backend and frontend

### Issue 2: "📨 Data received" but wrong type
**Problem**: Data type mismatch
**Check**: `data.type` in console
**Fix**: Verify backend sends `"type": "tool_call"`

### Issue 3: Data received but state doesn't update
**Problem**: React state issue
**Check**: 
- Look for "📋 Updated tool calls" in console
- Check React DevTools for state
- Check for React errors

**Fix**: 
- Verify `setToolCalls` is being called
- Check component re-renders
- Check for state mutation issues

### Issue 4: Tools not being called
**Problem**: LLM not using tools
**Check**:
- Backend logs for "🔧 TOOL CALL"
- LLM configuration
- Tool registration

**Fix**:
- Verify tools are passed to Agent
- Check LLM has tool calling enabled
- Try more explicit requests: "Use the identify_user tool to get my phone number"

## Testing Checklist

- [ ] Test UI button works (test call appears)
- [ ] Backend logs show "🔧 TOOL CALL"
- [ ] Backend logs show "📤 Sending tool_call"
- [ ] Frontend console shows "📨 Data received"
- [ ] Frontend console shows "📦 Parsed data"
- [ ] Frontend console shows "🔧 Tool call received"
- [ ] Frontend console shows "📋 Updated tool calls"
- [ ] UI shows tool call card

## What to Share

If still not working, share:

1. **Browser Console Output**:
   - All logs starting with 📨, 📦, 🔧, 📋
   - Any errors

2. **Backend Logs**:
   - All logs starting with 🔧, 📤
   - Any errors

3. **Test Button Result**:
   - Does test call appear when you click "🧪 Test UI"?

This will help identify exactly where the issue is!
