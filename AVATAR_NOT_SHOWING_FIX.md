# 🔧 Fix: Avatar Not Showing

## Issue
- No avatar participant joining (`bey-avatar-agent` not appearing)
- No video tracks published
- Frontend shows `Beyond Presence avatar integration - avatar ID: undefined`

## Root Causes

### 1. Backend: Avatar Session Not Starting
The Beyond Presence avatar session might not be starting. Check:

**Backend logs should show:**
```
Setting up beyond-presence avatar...
Setting up Beyond Presence avatar - Avatar ID: [your-id]
✅ Beyond Presence avatar session started successfully
```

**If you see errors instead:**
- `BEY_API_KEY must be set` → Add API key to backend `.env`
- `Beyond Presence plugin not installed` → Run `pip install 'livekit-agents[bey]'`
- `429 concurrency limit` → Stop other sessions or upgrade plan

### 2. Frontend: Environment Variables Not Set
Frontend needs `VITE_BEYOND_PRESENCE_AVATAR_ID` for display (optional but helpful).

## ✅ Step-by-Step Fix

### Step 1: Check Backend Configuration

**In `backend/.env`, ensure you have:**
```env
AVATAR_PROVIDER=beyond-presence
AVATAR_MODE=separate
BEY_API_KEY=your-api-key-here
BEY_AVATAR_ID=your-avatar-id-here
```

**Verify plugin is installed:**
```bash
cd backend
source venv/bin/activate
pip list | grep bey
# Should show: livekit-plugins-bey

# If not installed:
pip install 'livekit-agents[bey]'
```

### Step 2: Check Backend Logs

When you start the backend agent, look for:

**✅ Success:**
```
🔍 Avatar provider: 'beyond-presence', mode: 'separate'
Setting up beyond-presence avatar as separate participant (3 participants)...
Setting up Beyond Presence avatar - Avatar ID: [your-id]
✅ Beyond Presence avatar session started successfully
   Avatar will handle audio/video publishing - agent audio will be sent to avatar
```

**❌ Failure (check error message):**
```
❌ Avatar session creation failed - continuing without avatar
```

### Step 3: Check for Avatar Participant

**In backend logs, you should see:**
```
Participant connected: bey-avatar-agent
```

**If you don't see this:**
- Avatar session didn't start
- Check the error message above
- Verify API keys are correct

### Step 4: Frontend Configuration (Optional)

**In `frontend/.env`, add:**
```env
VITE_AVATAR_PROVIDER=beyond-presence
VITE_BEYOND_PRESENCE_AVATAR_ID=your-avatar-id-here
```

**Note**: This is optional - frontend will work without it, but it helps with display.

### Step 5: Restart Everything

1. **Restart backend agent** (after changing `.env`)
2. **Restart frontend dev server** (after changing `.env`)
3. **Clear browser cache** (optional but recommended)

## 🔍 Debugging Checklist

### Backend Issues

- [ ] `AVATAR_PROVIDER=beyond-presence` in `backend/.env`
- [ ] `BEY_API_KEY` set correctly
- [ ] `BEY_AVATAR_ID` set correctly
- [ ] Plugin installed: `pip install 'livekit-agents[bey]'`
- [ ] Backend logs show "✅ Beyond Presence avatar session started"
- [ ] Backend logs show "Participant connected: bey-avatar-agent"

### Frontend Issues

- [ ] `VITE_AVATAR_PROVIDER=beyond-presence` in `frontend/.env`
- [ ] Frontend console shows "Participant connected: bey-avatar-agent"
- [ ] Frontend console shows "Video track published from bey-avatar-agent"
- [ ] Video track subscribed successfully

## 🚨 Common Issues

### Issue: "Beyond Presence avatar integration - avatar ID: undefined"
**Fix**: Add to `frontend/.env`:
```env
VITE_BEYOND_PRESENCE_AVATAR_ID=your-avatar-id
```

### Issue: No "bey-avatar-agent" participant
**Fix**: 
1. Check backend logs for avatar session errors
2. Verify `BEY_API_KEY` and `BEY_AVATAR_ID` are set
3. Check for concurrency limit errors (429)

### Issue: "Avatar session creation failed"
**Fix**: 
1. Check the specific error in backend logs
2. Verify API keys are valid
3. Check Beyond Presence dashboard for active sessions

## 📝 Quick Test

1. **Set backend `.env`**:
   ```env
   AVATAR_PROVIDER=beyond-presence
   BEY_API_KEY=your-key
   BEY_AVATAR_ID=your-id
   ```

2. **Restart backend** and check logs for:
   ```
   ✅ Beyond Presence avatar session started successfully
   Participant connected: bey-avatar-agent
   ```

3. **Start frontend** and check console for:
   ```
   Participant connected: bey-avatar-agent
   Video track published from bey-avatar-agent
   Video track received from bey-avatar-agent
   ```

4. **Avatar should appear** in the UI!

## 🎯 Expected Behavior

**When working correctly:**
- Backend: 3 participants (user + agent + bey-avatar-agent)
- Frontend: Video track from bey-avatar-agent
- Avatar: Real Beyond Presence video displaying
- Sync: Avatar syncs with voice output

If you still don't see the avatar participant, share the backend logs and I'll help debug further!
