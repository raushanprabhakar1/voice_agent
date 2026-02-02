# SuperBryn AI Voice Agent - Backend

Backend implementation for the AI voice agent using LiveKit Agents.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and fill in your API keys:
```bash
cp .env.example .env
```

3. Set up Supabase database:
   - Create a new Supabase project
   - Run the SQL migrations in `supabase/migrations.sql`
   - Copy your Supabase URL and anon key to `.env`

4. Run the agent:
```bash
python agent.py dev
```

## Environment Variables

- `LIVEKIT_URL`: Your LiveKit server URL
- `LIVEKIT_API_KEY`: LiveKit API key
- `LIVEKIT_API_SECRET`: LiveKit API secret
- `DEEPGRAM_API_KEY`: Deepgram API key for STT
- `CARTESIA_API_KEY`: Cartesia API key for TTS
- `SUPABASE_URL`: Supabase project URL
- `SUPABASE_KEY`: Supabase anon key
- `LLM_PROVIDER`: One of `openai`, `azure`, `anthropic`, `together`, `openrouter`
- `LLM_MODEL`: Model name (e.g., `gpt-4o-mini`, `claude-3-haiku-20240307`)
- For Azure: `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_API_VERSION`, `AZURE_OPENAI_DEPLOYMENT_NAME`

## Database Schema

The database requires the following tables:
- `users`: Store user information (phone, name)
- `appointments`: Store appointment bookings
- `conversation_summaries`: Store conversation summaries

See `supabase/migrations.sql` for the schema.
