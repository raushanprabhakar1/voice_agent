# SuperBryn AI Voice Agent - Complete Solution

A web-based AI voice agent with visual avatar that can have natural conversations and book/retrieve appointments.

## 🎯 Features

- **Voice Conversation**: Real-time speech recognition and synthesis
- **Visual Avatar**: Synced with voice output (Beyond Presence/Tavus ready)
- **Appointment Management**: Book, retrieve, modify, and cancel appointments
- **Tool Call Visualization**: Real-time display of agent actions
- **Conversation Summary**: Auto-generated summary at end of call
- **Database Integration**: Supabase for persistent storage

## 📁 Project Structure

```
submission/
├── backend/          # LiveKit Agent (Python)
│   ├── agent.py      # Main agent implementation
│   ├── database.py   # Supabase database operations
│   ├── tools.py      # Tool definitions and execution
│   └── requirements.txt
├── frontend/         # React Web App
│   ├── src/
│   │   ├── components/
│   │   │   ├── VoiceAgent.tsx
│   │   │   ├── ToolCallDisplay.tsx
│   │   │   └── ConversationSummary.tsx
│   │   └── App.tsx
│   └── package.json
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- LiveKit Cloud account (free tier available)
- Supabase account (free tier available)
- API keys for:
  - Deepgram (200 hours/month free)
  - Cartesia (check current limits)
  - LLM provider (OpenAI/Claude/Together AI/OpenRouter)

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. Set up Supabase:
   - Create a new Supabase project
   - Run the SQL in `supabase/migrations.sql` to create tables
   - Copy your Supabase URL and anon key to `.env`

5. Run the agent:
```bash
python agent.py dev
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.example .env
# Add your LiveKit URL
```

4. Run development server:
```bash
npm run dev
```

5. Build for production:
```bash
npm run build
```

## 🔧 Configuration

### Backend Environment Variables

```env
# LiveKit
LIVEKIT_URL=wss://your-livekit-server.com
LIVEKIT_API_KEY=your-api-key
LIVEKIT_API_SECRET=your-api-secret

# Speech Services
DEEPGRAM_API_KEY=your-deepgram-key
CARTESIA_API_KEY=your-cartesia-key

# LLM (choose one)
LLM_PROVIDER=openai  # or azure, anthropic, together, openrouter
LLM_MODEL=gpt-4o-mini
OPENAI_API_KEY=your-key
# OR (Azure OpenAI)
LLM_PROVIDER=azure
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_API_KEY=your-key
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini
# OR
ANTHROPIC_API_KEY=your-key
# OR
TOGETHER_API_KEY=your-key
# OR
OPENROUTER_API_KEY=your-key

# Database
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
```

### Quick OpenRouter Setup

For OpenRouter (recommended for free credits), see [OPENROUTER_SETUP.md](OPENROUTER_SETUP.md) for detailed instructions.

**Quick setup:**
1. Sign up at [openrouter.ai](https://openrouter.ai/) and get your API key
2. Set in `.env`:
   ```env
   LLM_PROVIDER=openrouter
   LLM_MODEL=google/gemini-flash-1.5  # or any model from openrouter.ai/models
   OPENROUTER_API_KEY=sk-or-v1-your-key
   ```

### Azure OpenAI Setup

For Azure OpenAI, see [AZURE_OPENAI_SETUP.md](AZURE_OPENAI_SETUP.md) for detailed instructions.

**Quick setup:**
1. Create Azure OpenAI resource in [Azure Portal](https://portal.azure.com/)
2. Deploy a model in Azure OpenAI Studio
3. Set in `.env`:
   ```env
   LLM_PROVIDER=azure
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
   AZURE_OPENAI_API_KEY=your-key
   AZURE_OPENAI_API_VERSION=2024-02-15-preview
   AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini
   ```

### Frontend Environment Variables

```env
VITE_LIVEKIT_URL=wss://your-livekit-server.com
```

## 🎨 Avatar Integration

The frontend includes a placeholder avatar. To integrate Beyond Presence or Tavus:

### Tavus Integration

1. Install Tavus SDK:
```bash
npm install @tavus/react
```

2. Update `VoiceAgent.tsx`:
```typescript
import { Tavus } from '@tavus/react'

// Replace avatar section with:
<Tavus
  replicaId="your-replica-id"
  audioTrack={audioTrack}
  onReady={() => console.log('Avatar ready')}
/>
```

### Beyond Presence Integration

1. Install Beyond Presence SDK:
```bash
npm install @beyondpresence/react
```

2. Update `VoiceAgent.tsx` with their SDK components

## 📊 Database Schema

The Supabase database includes:

- **users**: User information (phone, name)
- **appointments**: Appointment bookings
- **conversation_summaries**: Conversation summaries with tool calls

See `backend/supabase/migrations.sql` for the complete schema.

## 🛠️ Tool Functions

The agent supports 7 tool functions:

1. **identify_user**: Get user's phone number
2. **fetch_slots**: Get available appointment slots (hardcoded)
3. **book_appointment**: Book an appointment
4. **retrieve_appointments**: Get user's appointments
5. **cancel_appointment**: Cancel an appointment
6. **modify_appointment**: Modify appointment details
7. **end_conversation**: End call and generate summary

## 🚢 Deployment

**📖 Full deployment guide**: See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

**⚡ Quick deploy**: See [QUICK_DEPLOY.md](QUICK_DEPLOY.md) for fastest setup.

### Quick Start

**Backend (Railway - Recommended)**:
1. Sign up at [railway.app](https://railway.app)
2. Create new project from GitHub
3. Set root directory: `backend`
4. Set start command: `python -m livekit.agents dev agent.py`
5. Add environment variables (see DEPLOYMENT_GUIDE.md)
6. Deploy

**Frontend (Vercel - Recommended)**:
1. Sign up at [vercel.com](https://vercel.com)
2. Import project from GitHub
3. Set root directory: `frontend`
4. Set build command: `npm run build`
5. Set output directory: `dist`
6. Add environment variables (see DEPLOYMENT_GUIDE.md)
7. Deploy

**Token API**: Automatically handled by Vercel (`api/token.ts`) or Netlify (`netlify/functions/token.js`)

For detailed deployment instructions, troubleshooting, and alternative platforms, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md).

## 📝 Known Limitations

1. **Avatar**: Currently uses placeholder. Full integration requires Tavus/Beyond Presence API keys
2. **Slots**: Appointment slots are hardcoded (9 AM, 11 AM, 2 PM, 4 PM for next 7 days)
3. **Error Handling**: Some edge cases may need additional handling
4. **Cost Tracking**: Optional bonus feature not yet implemented

## 🧪 Testing

1. Start the backend agent
2. Start the frontend dev server
3. Open the web app
4. Click "Start Voice Call"
5. Test the following flows:
   - Identify user with phone number
   - Fetch available slots
   - Book an appointment
   - Retrieve appointments
   - Cancel an appointment
   - Modify an appointment
   - End conversation and view summary

## 📚 Documentation

- [LiveKit Agents Docs](https://docs.livekit.io/agents/)
- [LiveKit Web SDK](https://docs.livekit.io/client-sdk-js/)
- [Supabase Docs](https://supabase.com/docs)
- [Deepgram Docs](https://developers.deepgram.com/)
- [Cartesia Docs](https://docs.cartesia.ai/)

## 🤝 Contributing

This is a submission for the SuperBryn AI Engineer Task. For questions or issues, please refer to the task requirements.

## 📄 License

This project is created for the SuperBryn AI Engineer Task.
