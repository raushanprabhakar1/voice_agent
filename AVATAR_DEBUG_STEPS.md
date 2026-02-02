# 🔍 Avatar Debugging Steps

## Current Issue
- No avatar participant (`bey-avatar-agent`) joining
- No video tracks published
- Frontend shows placeholder

## Step-by-Step Debugging

### Step 1: Check Backend Configuration

**Verify `backend/.env` has:**
```env
AVATAR_PROVIDER=beyond-presence
AVATAR_MODE=separate
BEY_API_KEY=your-actual-api-key
BEY_AVATAR_ID=your-actual-avatar-id
```

**⚠️ Important**: 
- `AVATAR_MODE` should be `separate` (or not set) for Beyond Presence
- If `AVATAR_MODE=direct`, avatar session won't start

### Step 2: Check Backend Logs

When you start the backend, look for these messages:

**✅ Success (what you should see):**
```
🔍 Avatar provider: 'beyond-presence', mode: 'separate'
Setting up beyond-presence avatar as separate participant (3 participants)...
Setting up Beyond Presence avatar - Avatar ID: [your-id]
   API Key: SET (length: XX)
✅ Beyond Presence avatar session started successfully
   Avatar will handle audio/video publishing - agent audio will be sent to avatar
Participant connected: bey-avatar-agent
```

**❌ Failure (what you might see):**
```
❌ Avatar session creation failed - continuing without avatar
```

**If you see failure, check the error above it:**
- `BEY_API_KEY must be set` → Add API key
- `Beyond Presence plugin not installed` → Run `pip install 'livekit-agents[bey]'`
- `429 concurrency limit` → Stop other sessions

### Step 3: Verify Plugin Installation

```bash
cd backend
source venv/bin/activate
pip list | grep bey
```

**Should show**: `livekit-plugins-bey`

**If not installed**:
```bash
pip install 'livekit-agents[bey]'
```

### Step 4: Check Frontend Console

**What you should see when avatar joins:**
```
👤 Participant connected: bey-avatar-agent
✅ Beyond Presence avatar participant joined!
   Avatar should publish video tracks soon...
📡 Track published: video from bey-avatar-agent
🎥 Video track published from bey-avatar-agent, subscribing...
✅ Beyond Presence avatar video track published!
🎥 Video track received from bey-avatar-agent
```

**What you're currently seeing:**
```
Checking participant: agent-AJ_...
```

**This means**: No avatar participant joined yet.

### Step 5: Common Issues & Fixes

#### Issue 1: `AVATAR_MODE=direct` is set
**Problem**: Direct mode skips avatar session creation
**Fix**: Remove `AVATAR_MODE=direct` or set `AVATAR_MODE=separate`

#### Issue 2: API Keys Not Set
**Problem**: `BEY_API_KEY` or `BEY_AVATAR_ID` missing
**Fix**: Add to `backend/.env` and restart

#### Issue 3: Plugin Not Installed
**Problem**: `ImportError: cannot import name 'bey'`
**Fix**: `pip install 'livekit-agents[bey]'`

#### Issue 4: Concurrency Limit
**Problem**: `429` error in logs
**Fix**: Stop other Beyond Presence sessions or upgrade plan

#### Issue 5: Wrong Provider Name
**Problem**: `AVATAR_PROVIDER=beyond_presence` (wrong)
**Fix**: Use `AVATAR_PROVIDER=beyond-presence` (with hyphen)

### Step 6: Quick Test

**1. Set backend `.env`**:
```env
AVATAR_PROVIDER=beyond-presence
# Don't set AVATAR_MODE (defaults to separate)
BEY_API_KEY=your-key
BEY_AVATAR_ID=your-id
```

**2. Restart backend** and watch logs for:
```
✅ Beyond Presence avatar session started successfully
Participant connected: bey-avatar-agent
```

**3. If you see those messages**: Avatar should work!

**4. If you don't see them**: Check the error message above

### Step 7: Frontend Environment (Optional)

**In `frontend/.env`** (optional, for display):
```env
VITE_AVATAR_PROVIDER=beyond-presence
VITE_BEYOND_PRESENCE_AVATAR_ID=your-id
```

**Note**: Frontend will work without this, but it helps with display.

---

## 🎯 Expected Flow

1. **Backend starts** → Avatar session created
2. **Avatar joins room** → `bey-avatar-agent` participant
3. **Avatar publishes video** → Video track available
4. **Frontend detects** → Subscribes to video track
5. **Avatar displays** → Video shows in UI

## 📊 Current Status

Based on your logs:
- ❌ No `bey-avatar-agent` participant
- ❌ No video tracks
- ✅ Agent participants working
- ✅ Audio tracks working

**This means**: Avatar session is not starting on backend.

**Next step**: Check backend logs for avatar session errors.

---

## 🔧 Quick Fix Checklist

- [ ] `AVATAR_PROVIDER=beyond-presence` in backend `.env`
- [ ] `AVATAR_MODE=separate` (or not set) in backend `.env`
- [ ] `BEY_API_KEY` set correctly
- [ ] `BEY_AVATAR_ID` set correctly
- [ ] Plugin installed: `pip install 'livekit-agents[bey]'`
- [ ] Backend restarted after changing `.env`
- [ ] Backend logs show "✅ Beyond Presence avatar session started"
- [ ] Backend logs show "Participant connected: bey-avatar-agent"

If all checked but still not working, share backend logs and I'll help debug!
