# Backend - SuperBryn Voice Agent

LiveKit Agent implementation for the AI voice agent using Python.

## 🏗️ Architecture

- **LiveKit Agents**: Real-time voice agent framework
- **Deepgram**: Speech-to-text (STT)
- **Cartesia**: Text-to-speech (TTS)
- **LLM**: OpenAI, Azure OpenAI, Anthropic, Together AI, or OpenRouter
- **Supabase**: Database for persistence
- **Avatar Support**: Tavus/Beyond Presence integration ready

## 📦 Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   Create a `.env` file with all required variables (see Configuration section)

3. **Set up Supabase database**:
   - Create a Supabase project
   - Run the SQL in `supabase/migrations.sql`
   - Copy URL and anon key to `.env`

## 🚀 Running the Agent

### Development Mode

```bash
python -m livekit.agents dev agent.py
```

### Production Mode

```bash
python -m livekit.agents start agent.py
```

## ⚙️ Configuration

### Required Environment Variables

```env
# LiveKit
LIVEKIT_URL=wss://your-livekit-server.com
LIVEKIT_API_KEY=your-api-key
LIVEKIT_API_SECRET=your-api-secret

# Speech Services
DEEPGRAM_API_KEY=your-deepgram-key
CARTESIA_API_KEY=your-cartesia-key

# LLM (choose one provider)
LLM_PROVIDER=openai  # or azure, anthropic, together, openrouter
LLM_MODEL=gpt-4o-mini

# Provider-specific keys
OPENAI_API_KEY=your-key
# OR for Azure:
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_API_KEY=your-key
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini
# OR for Anthropic:
ANTHROPIC_API_KEY=sk-ant-...
# OR for Together:
TOGETHER_API_KEY=...
# OR for OpenRouter:
OPENROUTER_API_KEY=sk-or-v1-...

# Database
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
```

### Optional Environment Variables

```env
# Avatar Configuration
AVATAR_PROVIDER=placeholder  # or tavus, beyond-presence
ENABLE_AVATAR_VIDEO=true
AVATAR_VIDEO_WIDTH=640
AVATAR_VIDEO_HEIGHT=360
AVATAR_VIDEO_FPS=15

# Avatar API Keys (if using Tavus/Beyond Presence)
TAVUS_API_KEY=your-key
TAVUS_REPLICA_ID=your-replica-id
BEYOND_PRESENCE_API_KEY=your-key
BEYOND_PRESENCE_AVATAR_ID=your-avatar-id
```

## 📁 File Structure

```
backend/
├── agent.py              # Main agent entrypoint and logic
├── database.py           # Supabase database operations
├── tools.py              # Tool definitions and execution
├── avatar_integration.py # Avatar integration (Tavus/Beyond Presence)
├── avatar_video.py       # Video track publishing
├── check_agent.py        # Agent verification script
├── requirements.txt      # Python dependencies
└── supabase/
    └── migrations.sql   # Database schema
```

## 🛠️ Tool Functions

The agent implements 7 tool functions:

1. **`identify_user`**: Ask for and store user's phone number
2. **`fetch_slots`**: Get available appointment slots (filters out booked slots)
3. **`book_appointment`**: Book an appointment (prevents double-booking)
4. **`retrieve_appointments`**: Get user's appointments from database
5. **`cancel_appointment`**: Cancel an appointment by ID
6. **`modify_appointment`**: Modify appointment date/time/notes
7. **`end_conversation`**: End call and generate summary

### Key Implementation Details

- **Smart Slot Filtering**: `fetch_slots` queries the database for booked appointments and only returns available slots
- **Double-Booking Prevention**: `book_appointment` checks for conflicts before creating the appointment
- **Real-time Data Channels**: Tool calls are sent to frontend via LiveKit data channels
- **Conversation Summaries**: Auto-generated summaries with all tool calls and key points

## 📊 Database Schema

The Supabase database includes:

- **`users`**: User information (phone, name, created_at)
- **`appointments`**: Appointment bookings (date, time, status, notes, user_phone)
- **`conversation_summaries`**: Conversation summaries with tool calls

See `supabase/migrations.sql` for the complete schema.

## 🎨 Avatar Integration

The backend supports multiple avatar modes:

### Placeholder Mode (Default)
- Generates animated test pattern video
- No external dependencies
- Good for testing and development

### Tavus Integration
- Real-time avatar rendering
- Requires Tavus API key and replica ID
- Set `AVATAR_PROVIDER=tavus`

### Beyond Presence Integration
- Real-time avatar rendering
- Requires Beyond Presence API key and avatar ID
- Set `AVATAR_PROVIDER=beyond-presence`

The avatar video is published as a LiveKit video track that the frontend subscribes to.

## 🔍 Event Handling

The agent handles several events:

- **`UserInputTranscribedEvent`**: User speech transcribed
- **`ConversationItemAddedEvent`**: Message added to conversation
- **`FunctionToolsExecutedEvent`**: Tool call executed (sent to frontend)
- **Room disconnection**: Generates and sends conversation summary

## 🧪 Testing

### Verify Agent Connection

```bash
python check_agent.py
```

This will verify:
- Environment variables are set
- LiveKit connection works
- Agent can register with LiveKit

### Test Database

The `database.py` module includes methods for:
- Creating users
- Fetching available slots (with booking filtering)
- Booking appointments
- Retrieving appointments
- Cancelling/modifying appointments
- Saving conversation summaries

## 🚢 Deployment

For deployment instructions, see the main [DEPLOY_STEP_BY_STEP.md](../DEPLOY_STEP_BY_STEP.md).

### Quick Deployment (Railway)

1. Create Railway project from GitHub
2. Set root directory: `backend`
3. Set start command: `python -m livekit.agents dev agent.py`
4. Add all environment variables
5. Deploy

## 📝 Logging

The agent includes comprehensive logging:

- Startup: Environment variable checks, database initialization
- Connection: Room connection, participant events
- Tool calls: All tool executions with arguments and results
- Errors: Detailed error messages with stack traces

Check logs in:
- Development: Terminal output
- Production: Railway/Render logs

## 🔧 Troubleshooting

### Agent Not Connecting

- Check `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`
- Verify agent logs show "registered_workers"
- Check LiveKit dashboard for agent status

### Database Errors

- Verify `SUPABASE_URL` and `SUPABASE_KEY`
- Check migrations ran successfully
- Verify tables exist in Supabase dashboard

### Tool Call Errors

- Check tool function implementations in `tools.py`
- Verify database methods in `database.py`
- Check logs for specific error messages

### Avatar Not Publishing

- Verify `ENABLE_AVATAR_VIDEO=true`
- Check `AVATAR_PROVIDER` is set correctly
- For Tavus/Beyond Presence: Verify API keys are set
- Check logs for video publishing errors
