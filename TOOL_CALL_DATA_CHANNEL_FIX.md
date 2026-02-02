# 🔧 Tool Call Data Channel Fix

## Issue
Tool calls are not appearing in the UI. The component shows "0 calls" even when tools are being executed.

## Root Cause Analysis

The issue is likely in the data channel communication between backend and frontend. Let me check:

1. **Backend sending**: Are tool calls being sent?
2. **Frontend receiving**: Is data being received?
3. **Topic filtering**: Is topic matching working?
4. **Data parsing**: Is JSON parsing working?

## Changes Made

### 1. Enhanced Backend Logging
- ✅ Logs when sending tool calls
- ✅ Logs data payload
- ✅ Logs room participant count
- ✅ Tries sending with and without topic
- ✅ Better error handling

### 2. Enhanced Frontend Logging
- ✅ Logs all received data
- ✅ Shows payload preview
- ✅ Shows topic (or "no topic")
- ✅ Logs parsed data type

### 3. Fallback Mechanism
- ✅ Backend tries sending with topic first
- ✅ Falls back to sending without topic if that fails
- ✅ Frontend accepts data regardless of topic

## How to Debug

### Step 1: Check Browser Console

When you trigger a tool call, you should see:

```
📨 Data received: {kind: 1, topic: "tool_calls", ...}
📦 Parsed data: {type: "tool_call", name: "identify_user", ...}
   Type: tool_call
🔧 Tool call received: identify_user {...}
📋 Updated tool calls: 1
🔧 ToolCallDisplay: toolCalls updated: 1
```

**If you see "📨 Data received" but no "📦 Parsed data":**
- JSON parsing is failing
- Check the payload preview in the log

**If you don't see "📨 Data received" at all:**
- Data channel not working
- Check LiveKit connection
- Check backend logs for sending

### Step 2: Check Backend Logs

You should see:

```
🔧 TOOL CALL: identify_user
📤 Sending tool_call to frontend: identify_user
   Data: {"type":"tool_call","name":"identify_user",...}
   Room participants: 1
   ✅ Data sent with topic 'tool_calls'
```

**If you see errors:**
- Check the error message
- Backend will try without topic as fallback

### Step 3: Test Data Channel

1. **Trigger a tool call** (e.g., say "I want to book an appointment")
2. **Check backend logs** for "📤 Sending tool_call"
3. **Check frontend console** for "📨 Data received"
4. **Verify data is parsed** correctly

## Common Issues & Fixes

### Issue 1: No "📨 Data received" in console
**Problem**: Data channel not working
**Fix**: 
- Check LiveKit connection status
- Verify room is connected
- Check network tab for WebSocket connection
- Restart backend and frontend

### Issue 2: "📨 Data received" but wrong topic
**Problem**: Topic mismatch
**Fix**: 
- Backend now tries without topic as fallback
- Frontend accepts all topics
- Should work now

### Issue 3: "📨 Data received" but parsing fails
**Problem**: Invalid JSON
**Fix**: 
- Check payload preview in console
- Verify backend is sending valid JSON
- Check for encoding issues

### Issue 4: Data received but state doesn't update
**Problem**: React state issue
**Fix**: 
- Check for React errors in console
- Verify `setToolCalls` is being called
- Check component re-renders

## Testing Steps

1. **Start backend** and frontend
2. **Open browser console** (F12)
3. **Start voice call**
4. **Say**: "I want to book an appointment"
5. **Watch console** for:
   - Backend: "📤 Sending tool_call"
   - Frontend: "📨 Data received"
   - Frontend: "🔧 Tool call received"
   - UI: Tool call appears

## Expected Behavior

When working correctly:
1. User speaks → LLM calls tool
2. Backend logs: "🔧 TOOL CALL: identify_user"
3. Backend sends: "📤 Sending tool_call to frontend"
4. Frontend receives: "📨 Data received"
5. Frontend parses: "📦 Parsed data"
6. Frontend updates: "📋 Updated tool calls: 1"
7. UI shows: Tool call card

## Summary

The enhanced logging and fallback mechanism should help identify and fix the issue. The backend now:
- ✅ Logs detailed information when sending
- ✅ Tries multiple methods (with/without topic)
- ✅ Provides better error messages

The frontend now:
- ✅ Logs all received data
- ✅ Shows payload preview
- ✅ Accepts data regardless of topic

**Check the console logs to see where the data flow is breaking!**
