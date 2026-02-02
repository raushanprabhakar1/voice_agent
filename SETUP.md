# Setup Guide

This guide will help you set up the SuperBryn Voice Agent from scratch.

## Step 1: Get API Keys

### 1.1 LiveKit
1. Sign up at [LiveKit Cloud](https://cloud.livekit.io/) (free tier available)
2. Create a new project
3. Copy your:
   - Server URL (wss://...)
   - API Key
   - API Secret

### 1.2 Deepgram
1. Sign up at [Deepgram](https://deepgram.com/) (200 hours/month free)
2. Create an API key
3. Copy your API key

### 1.3 Cartesia
1. Sign up at [Cartesia](https://cartesia.ai/)
2. Check current free tier limits
3. Create an API key
4. Copy your API key

### 1.4 LLM Provider (Choose One)

**Option A: OpenAI**
1. Sign up at [OpenAI](https://platform.openai.com/)
2. Add payment method (required)
3. Create an API key
4. Copy your API key

**Option B: Anthropic (Claude)**
1. Sign up at [Anthropic](https://console.anthropic.com/)
2. Add payment method (required)
3. Create an API key
4. Copy your API key

**Option C: Together AI**
1. Sign up at [Together AI](https://together.ai/)
2. Get free credits
3. Create an API key
4. Copy your API key

**Option D: OpenRouter**
1. Sign up at [OpenRouter](https://openrouter.ai/)
2. Get free credits
3. Create an API key
4. Copy your API key

### 1.5 Supabase
1. Sign up at [Supabase](https://supabase.com/) (free tier available)
2. Create a new project
3. Go to Settings > API
4. Copy your:
   - Project URL
   - anon/public key

## Step 2: Set Up Database

1. Open your Supabase project
2. Go to SQL Editor
3. Run the SQL from `backend/supabase/migrations.sql`
4. Verify tables are created:
   - `users`
   - `appointments`
   - `conversation_summaries`

## Step 3: Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env with your API keys
# Use your preferred editor (nano, vim, code, etc.)
nano .env
```

Fill in your `.env` file:
```env
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your-api-key
LIVEKIT_API_SECRET=your-api-secret

DEEPGRAM_API_KEY=your-deepgram-key
CARTESIA_API_KEY=your-cartesia-key

LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
OPENAI_API_KEY=your-openai-key

SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-key
```

## Step 4: Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Edit .env
nano .env
```

Fill in your `.env` file:
```env
VITE_LIVEKIT_URL=wss://your-project.livekit.cloud
```

## Step 5: Set Up Token API

### For Vercel:
1. The `api/token.ts` file is already created
2. Add environment variables in Vercel dashboard:
   - `LIVEKIT_API_KEY`
   - `LIVEKIT_API_SECRET`
   - `LIVEKIT_URL`

### For Netlify:
1. The `netlify/functions/token.js` file is already created
2. Install livekit-server-sdk in your Netlify function:
   ```bash
   cd netlify/functions
   npm init -y
   npm install livekit-server-sdk
   ```
3. Add environment variables in Netlify dashboard

## Step 6: Run Locally

### Terminal 1 - Backend:
```bash
cd backend
python agent.py dev
```

### Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

### Terminal 3 - Token API (if testing locally):
For local testing, you can use a simple Node.js server or test directly with deployed functions.

## Step 7: Test

1. Open http://localhost:3000 (or your frontend URL)
2. Click "Start Voice Call"
3. Allow microphone access
4. Try saying: "I'd like to book an appointment"
5. Follow the agent's prompts

## Troubleshooting

### Backend Issues
- **Import errors**: Make sure all dependencies are installed
- **API key errors**: Verify your `.env` file has all keys
- **Database errors**: Check Supabase connection and table creation

### Frontend Issues
- **Connection errors**: Verify LiveKit URL and token API
- **Audio issues**: Check browser permissions for microphone
- **Build errors**: Make sure Node.js version is 18+

### Common Issues
- **"Token endpoint not implemented"**: Set up the serverless function for your platform
- **"Room connection failed"**: Check LiveKit credentials
- **"No audio"**: Check browser permissions and audio settings

## Next Steps

- Integrate Tavus or Beyond Presence for avatar
- Customize the agent's personality in `backend/agent.py`
- Add more appointment slots or dynamic scheduling
- Implement cost tracking (optional bonus)
