# Quick Start Guide

Get up and running in 5 minutes!

## Prerequisites Checklist

- [ ] Python 3.9+ installed
- [ ] Node.js 18+ installed
- [ ] LiveKit Cloud account
- [ ] Deepgram API key
- [ ] Cartesia API key
- [ ] LLM API key (OpenAI/Claude/Together/OpenRouter)
- [ ] Supabase account

## Quick Setup

### 1. Backend (2 minutes)

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your keys
python agent.py dev
```

### 2. Frontend (2 minutes)

```bash
cd frontend
npm install
cp .env.example .env
# Add VITE_LIVEKIT_URL to .env
npm run dev
```

### 3. Database (1 minute)

1. Go to Supabase SQL Editor
2. Run `backend/supabase/migrations.sql`
3. Done!

## Test It

1. Open http://localhost:3000
2. Click "Start Voice Call"
3. Say: "I want to book an appointment"
4. Follow the prompts!

## What to Test

✅ Voice recognition works
✅ Agent responds with voice
✅ Tool calls appear in UI
✅ Can book an appointment
✅ Can retrieve appointments
✅ Summary appears at end

## Common Commands

**Book appointment:**
- "I'd like to book an appointment"
- "Can I schedule for tomorrow at 2 PM?"

**Retrieve appointments:**
- "Show me my appointments"
- "What appointments do I have?"

**Cancel appointment:**
- "Cancel my appointment"
- "I need to cancel"

**End call:**
- "Goodbye"
- "That's all, thank you"

## Need Help?

See `SETUP.md` for detailed instructions or `README.md` for full documentation.
