# SuperBryn AI Voice Agent

A production-ready web-based AI voice agent with visual avatar that can have natural conversations and book/retrieve appointments.

## 🎯 Features

- **🎙️ Real-time Voice Conversation**: Speech-to-text (Deepgram) and text-to-speech (Cartesia) for natural conversations
- **👤 Visual Avatar**: LiveKit video tracks synced with voice output (Beyond Presence/Tavus ready)
- **📅 Appointment Management**: Book, retrieve, modify, and cancel appointments with intelligent slot filtering
- **🔧 Tool Call Visualization**: Real-time display of agent actions in an intuitive UI
- **📝 Conversation Summary**: Auto-generated summary at end of call with all tool calls and key points
- **💾 Database Integration**: Supabase for persistent storage of users, appointments, and summaries
- **⚡ Optimized Slot Booking**: Only returns available slots (filters out booked appointments automatically)

## 📁 Project Structure

```
submission/
├── backend/                    # LiveKit Agent (Python)
│   ├── agent.py               # Main agent implementation
│   ├── database.py            # Supabase database operations
│   ├── tools.py               # Tool definitions and execution
│   ├── avatar_integration.py  # Avatar integration (Tavus/Beyond Presence)
│   ├── avatar_video.py        # Video track publishing
│   ├── supabase/
│   │   └── migrations.sql    # Database schema
│   └── requirements.txt
├── frontend/                   # React Web App (Vite)
│   ├── src/
│   │   ├── components/
│   │   │   ├── VoiceAgent.tsx         # Main voice agent UI
│   │   │   ├── AvatarPlayer.tsx       # Avatar rendering
│   │   │   ├── ToolCallDisplay.tsx     # Tool call visualization
│   │   │   └── ConversationSummary.tsx # Summary display
│   │   ├── App.tsx            # Main app component
│   │   └── main.tsx
│   ├── api/
│   │   └── token.ts          # Vercel serverless function for tokens
│   ├── netlify/
│   │   └── functions/
│   │       └── token.js       # Netlify function for tokens
│   └── package.json
├── DEPLOY_STEP_BY_STEP.md    # Detailed deployment guide
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+**
- **Node.js 18+**
- **LiveKit Cloud account** ([sign up](https://cloud.livekit.io/) - free tier available)
- **Supabase account** ([sign up](https://supabase.com/) - free tier available)
- **API Keys**:
  - **Deepgram** ([get key](https://deepgram.com/)) - 200 hours/month free
  - **Cartesia** ([get key](https://cartesia.ai/)) - check current limits
  - **LLM Provider** (choose one):
    - OpenAI ([get key](https://platform.openai.com/))
    - Azure OpenAI ([setup guide](https://azure.microsoft.com/en-us/products/ai-services/openai-service))
    - Anthropic Claude ([get key](https://console.anthropic.com/))
    - Together AI ([get key](https://together.ai/))
    - OpenRouter ([get key](https://openrouter.ai/)) - recommended for free credits

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the `backend` directory:
   ```env
   # LiveKit
   LIVEKIT_URL=wss://your-livekit-server.com
   LIVEKIT_API_KEY=your-api-key
   LIVEKIT_API_SECRET=your-api-secret
   
   # Speech Services
   DEEPGRAM_API_KEY=your-deepgram-key
   CARTESIA_API_KEY=your-cartesia-key
   
   # LLM (choose one provider)
   LLM_PROVIDER=openai
   LLM_MODEL=gpt-4o-mini
   OPENAI_API_KEY=your-key
   
   # Database
   SUPABASE_URL=your-supabase-url
   SUPABASE_KEY=your-supabase-key
   
   # Avatar (optional)
   AVATAR_PROVIDER=placeholder
   ENABLE_AVATAR_VIDEO=true
   ```

4. **Set up Supabase database**:
   - Create a new Supabase project at [supabase.com](https://supabase.com)
   - Go to SQL Editor
   - Run the SQL in `backend/supabase/migrations.sql` to create tables
   - Copy your Supabase URL and anon key to `.env`

5. **Run the agent**:
   ```bash
   python -m livekit.agents dev agent.py
   ```

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Set up environment variables**:
   Create a `.env` file in the `frontend` directory:
   ```env
   VITE_LIVEKIT_URL=wss://your-livekit-server.com
   VITE_AVATAR_PROVIDER=livekit-video
   ```

4. **Run development server**:
   ```bash
   npm run dev
   ```

5. **Build for production**:
   ```bash
   npm run build
   ```

## 🔧 Configuration

### LLM Provider Options

#### OpenAI
```env
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
OPENAI_API_KEY=sk-...
```

#### Azure OpenAI
```env
LLM_PROVIDER=azure
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_API_KEY=your-key
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini
```

#### Anthropic Claude
```env
LLM_PROVIDER=anthropic
LLM_MODEL=claude-3-haiku-20240307
ANTHROPIC_API_KEY=sk-ant-...
```

#### Together AI
```env
LLM_PROVIDER=together
LLM_MODEL=meta-llama/Llama-3-8b-chat-hf
TOGETHER_API_KEY=...
```

#### OpenRouter (Recommended for free credits)
```env
LLM_PROVIDER=openrouter
LLM_MODEL=google/gemini-flash-1.5
OPENROUTER_API_KEY=sk-or-v1-...
```

### Avatar Configuration

The agent supports multiple avatar modes:

- **Placeholder** (default): Simple animated test pattern
- **Tavus**: Real-time avatar rendering (requires Tavus API key)
- **Beyond Presence**: Real-time avatar rendering (requires Beyond Presence API key)

Set in `.env`:
```env
AVATAR_PROVIDER=placeholder  # or tavus, beyond-presence
ENABLE_AVATAR_VIDEO=true
AVATAR_VIDEO_WIDTH=640
AVATAR_VIDEO_HEIGHT=360
AVATAR_VIDEO_FPS=15
```

## 🛠️ Tool Functions

The agent supports 7 tool functions for appointment management:

1. **`identify_user`**: Ask for and store user's phone number to identify them
2. **`fetch_slots`**: Get available appointment slots (automatically filters out booked slots)
3. **`book_appointment`**: Book an appointment for user (prevents double-booking)
4. **`retrieve_appointments`**: Fetch past appointments of user from database
5. **`cancel_appointment`**: Mark an appointment as cancelled
6. **`modify_appointment`**: Change date/time of an appointment
7. **`end_conversation`**: End call and generate conversation summary

### Key Features

- **Smart Slot Filtering**: `fetch_slots` only returns available slots (booked slots are automatically excluded)
- **Double-Booking Prevention**: `book_appointment` checks for conflicts before booking
- **Real-time UI Updates**: All tool calls are displayed in the frontend in real-time
- **Conversation Summaries**: Automatic summary generation with all tool calls and key points

## 📊 Database Schema

The Supabase database includes three main tables:

- **`users`**: User information (phone, name, created_at)
- **`appointments`**: Appointment bookings (date, time, status, notes)
- **`conversation_summaries`**: Conversation summaries with tool calls and key points

See `backend/supabase/migrations.sql` for the complete schema.

## 🚢 Deployment

For detailed step-by-step deployment instructions, see **[DEPLOY_STEP_BY_STEP.md](./DEPLOY_STEP_BY_STEP.md)**.

### Quick Deployment Summary

**Backend (Railway - Recommended)**:
1. Sign up at [railway.app](https://railway.app)
2. Create new project from GitHub repo
3. Set root directory: `backend`
4. Set start command: `python agent.py`
5. Add all environment variables
6. Deploy

**Frontend (Vercel - Recommended)**:
1. Sign up at [vercel.com](https://vercel.com)
2. Import project from GitHub
3. Set root directory: `frontend`
4. Set build command: `npm run build`
5. Set output directory: `dist`
6. Add environment variables (VITE_* for frontend, LIVEKIT_* for token API)
7. Deploy

**Token API**: Automatically handled by Vercel (`api/token.ts`) or Netlify (`netlify/functions/token.js`)

## 🧪 Testing

### Local Testing

1. **Start backend agent**:
   ```bash
   cd backend
   python -m livekit.agents dev agent.py
   ```

2. **Start frontend dev server**:
   ```bash
   cd frontend
   npm run dev
   ```

3. **Test the flow**:
   - Open the web app (usually `http://localhost:5173`)
   - Click "Start Voice Call"
   - Grant microphone permission
   - Test the following:
     - ✅ Identify user with phone number
     - ✅ Fetch available slots (should only show unbooked slots)
     - ✅ Book an appointment
     - ✅ Retrieve appointments
     - ✅ Cancel an appointment
     - ✅ Modify an appointment
     - ✅ End conversation and view summary
     - ✅ Verify tool calls appear in UI
     - ✅ Verify avatar displays (if enabled)

### Production Testing

After deployment:
1. Visit your deployed frontend URL
2. Test the complete flow
3. Check backend logs (Railway dashboard)
4. Verify database entries (Supabase dashboard)

## 📚 Documentation

- **[DEPLOY_STEP_BY_STEP.md](./DEPLOY_STEP_BY_STEP.md)**: Complete deployment guide
- **[Backend README](./backend/README.md)**: Backend-specific documentation
- **[Frontend README](./frontend/README.md)**: Frontend-specific documentation

### External Documentation

- [LiveKit Agents Docs](https://docs.livekit.io/agents/)
- [LiveKit Web SDK](https://docs.livekit.io/client-sdk-js/)
- [Supabase Docs](https://supabase.com/docs)
- [Deepgram Docs](https://developers.deepgram.com/)
- [Cartesia Docs](https://docs.cartesia.ai/)

## 🎨 Avatar Integration

The frontend includes full avatar support with LiveKit video tracks. The backend can publish video directly or integrate with third-party services:

- **LiveKit Video**: Direct video track publishing (default)
- **Tavus**: Real-time avatar rendering (requires Tavus API)
- **Beyond Presence**: Real-time avatar rendering (requires Beyond Presence API)

See `backend/avatar_integration.py` and `frontend/src/components/AvatarPlayer.tsx` for implementation details.

## 🔍 Key Implementation Details

### Optimized Slot Booking

The `fetch_slots` tool automatically filters out booked appointments, so the agent only sees available slots. This means:
- No need to iterate through all slots
- Agent can book the first available slot directly
- Prevents showing unavailable slots to users

### Real-time Tool Call Visualization

All tool calls are sent to the frontend via LiveKit data channels and displayed in real-time:
- Tool call name and arguments
- Execution status (pending/success/error)
- Results with formatted JSON
- Expandable details for each call

### Conversation Summaries

At the end of each conversation:
- LLM generates a comprehensive summary
- Includes all tool calls made
- Extracts key points and user preferences
- Saved to database and sent to frontend
- Displayed in a user-friendly format

## 📝 Known Limitations

1. **Avatar**: Currently uses placeholder by default. Full integration requires Tavus/Beyond Presence API keys
2. **Slot Times**: Hardcoded to 9 AM, 11 AM, 2 PM, 4 PM (can be modified in `database.py`)
3. **Slot Range**: Shows slots for next 7 days (can be modified in `database.py`)

## 🤝 Contributing

This is a submission for the SuperBryn AI Engineer Task. For questions or issues, please refer to the task requirements.

## 📄 License

This project is created for the SuperBryn AI Engineer Task.
