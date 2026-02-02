# 🔧 Tool Call UI Debugging Guide

## Issue: Tool Calls Not Showing in UI

### What I've Added

1. **Enhanced Logging**:
   - Backend logs when sending tool calls/results
   - Frontend logs when receiving data
   - Component logs when tool calls update

2. **Better Data Handling**:
   - Accepts both RELIABLE and LOSSY data packets
   - Better error handling and logging
   - Improved argument parsing

3. **UI Improvements**:
   - Shows "0 calls" when empty (instead of hiding)
   - Better tool result matching (checks multiple recent calls)

4. **Backend Improvements**:
   - Explicit `reliable=True` flag
   - Better error logging with traceback
   - Argument parsing before sending

---

## 🔍 How to Debug

### Step 1: Check Browser Console

Open browser DevTools (F12) and look for:

**✅ Good signs:**
```
📨 Data received: {kind: 0, topic: "tool_calls", ...}
📦 Parsed data: {type: "tool_call", name: "identify_user", ...}
🔧 Tool call received: identify_user {...}
📋 Updated tool calls: 1
🔧 ToolCallDisplay: toolCalls updated: 1 [...]
```

**❌ Bad signs:**
```
⚠️ Data packet kind not RELIABLE or LOSSY: ...
❌ Error parsing data message: ...
```

### Step 2: Check Backend Logs

Look for:
```
🔧 TOOL CALL: identify_user
📤 Sending tool_call to frontend: identify_user
📤 Sending tool_result to frontend: identify_user
```

**If you see errors:**
```
❌ Error sending tool call to frontend: ...
```

### Step 3: Verify Data Channel

1. **Check if data is being sent**:
   - Backend should log "📤 Sending tool_call to frontend"
   - If not, tool might not be called

2. **Check if data is being received**:
   - Frontend should log "📨 Data received"
   - If not, data channel might not be working

3. **Check if data is parsed**:
   - Frontend should log "📦 Parsed data"
   - If not, JSON parsing might be failing

4. **Check if state updates**:
   - Frontend should log "📋 Updated tool calls"
   - Component should log "🔧 ToolCallDisplay: toolCalls updated"

---

## 🐛 Common Issues

### Issue 1: No "Data received" logs
**Problem**: Data channel not working
**Fix**: 
- Check LiveKit connection
- Verify room is connected
- Check network tab for WebSocket connection

### Issue 2: "Data received" but no "Parsed data"
**Problem**: JSON parsing failing
**Fix**: 
- Check payload format
- Verify data is valid JSON
- Check for encoding issues

### Issue 3: "Parsed data" but no "Tool call received"
**Problem**: Wrong data type
**Fix**: 
- Check `data.type === 'tool_call'`
- Verify backend sends correct type

### Issue 4: "Tool call received" but UI doesn't update
**Problem**: State not updating
**Fix**: 
- Check React state updates
- Verify component re-renders
- Check for React errors in console

### Issue 5: Tool calls appear but results don't
**Problem**: Result matching failing
**Fix**: 
- Check tool result name matches
- Verify result is sent after call
- Check timing (result might come before call)

---

## ✅ Testing Steps

1. **Start the call**
2. **Trigger a tool call** (e.g., ask to book appointment)
3. **Check browser console** for logs
4. **Check backend logs** for sending messages
5. **Verify UI updates** with tool call

---

## 📊 Expected Flow

1. **User speaks**: "I want to book an appointment"
2. **Backend**: LLM calls `identify_user` tool
3. **Backend logs**: `🔧 TOOL CALL: identify_user`
4. **Backend sends**: `📤 Sending tool_call to frontend: identify_user`
5. **Frontend receives**: `📨 Data received`
6. **Frontend parses**: `📦 Parsed data: {type: "tool_call", ...}`
7. **Frontend logs**: `🔧 Tool call received: identify_user`
8. **Frontend updates**: `📋 Updated tool calls: 1`
9. **Component logs**: `🔧 ToolCallDisplay: toolCalls updated: 1`
10. **UI shows**: Tool call card appears

---

## 🎯 Quick Fixes

### If nothing appears:
1. Check browser console for errors
2. Check backend logs for sending messages
3. Verify LiveKit connection is active
4. Try refreshing the page

### If tool calls appear but no results:
1. Check if results are being sent
2. Verify result name matches call name
3. Check timing (wait a moment)
4. Look for errors in console

### If UI is blank:
1. Check if component is rendering
2. Verify `toolCalls.length > 0`
3. Check for CSS issues
4. Verify component is in DOM

---

## 📝 Summary

The enhanced logging will help identify where the issue is:
- **Backend not sending** → Check backend logs
- **Frontend not receiving** → Check data channel
- **Frontend not parsing** → Check JSON format
- **State not updating** → Check React state
- **UI not rendering** → Check component

Use the console logs to trace the data flow and identify the issue!
