# Tavus & Beyond Presence Avatar Integration

This guide shows you how to integrate real avatars using Tavus or Beyond Presence with LiveKit's built-in avatar support.

## Quick Start

### Option 1: Tavus Integration

1. **Install the Tavus plugin**:
   ```bash
   cd backend
   source venv/bin/activate  # or activate your virtual environment
   pip install 'livekit-agents[tavus]'
   ```

2. **Get your Tavus credentials**:
   - Sign up at [Tavus](https://tavus.io)
   - Create a Replica (your avatar model)
   - Create a Persona with:
     - `pipeline_mode: echo`
     - `transport_type: livekit`
   - Get your API key, Replica ID, and Persona ID

3. **Set environment variables** in `backend/.env`:
   ```env
   AVATAR_PROVIDER=tavus
   TAVUS_API_KEY=your-tavus-api-key
   TAVUS_REPLICA_ID=your-replica-id
   TAVUS_PERSONA_ID=your-persona-id  # Optional, but recommended
   ```

4. **Restart the backend agent**:
   ```bash
   cd backend
   ./venv/bin/python -m livekit.agents dev agent.py
   ```

5. **The avatar will automatically**:
   - Join the LiveKit room
   - Publish synchronized video and audio tracks
   - Receive audio from the agent for lip-sync
   - Handle all video rendering on Tavus servers (no local CPU usage!)

### Option 2: Beyond Presence Integration

1. **Install the Beyond Presence plugin**:
   ```bash
   cd backend
   source venv/bin/activate
   pip install 'livekit-agents[bey]'
   ```

2. **Get your Beyond Presence credentials**:
   - Sign up at [Beyond Presence](https://beyondpresence.ai)
   - Create or select an avatar
   - Get your API key and Avatar ID

3. **Set environment variables** in `backend/.env`:
   ```env
   AVATAR_PROVIDER=beyond-presence
   BEY_API_KEY=your-api-key
   BEY_AVATAR_ID=your-avatar-id
   
   # Alternative naming (also supported):
   # BEYOND_PRESENCE_API_KEY=your-api-key
   # BEYOND_PRESENCE_AVATAR_ID=your-avatar-id
   ```

4. **Restart the backend agent**:
   ```bash
   cd backend
   ./venv/bin/python -m livekit.agents dev agent.py
   ```

5. **The avatar will automatically**:
   - Join the LiveKit room
   - Publish synchronized video and audio tracks
   - Receive audio from the agent for lip-sync
   - Handle all video rendering on Beyond Presence servers

## How It Works

1. **Avatar Session Setup**: The `avatar_integration.py` module creates an `AvatarSession` using LiveKit's built-in plugins
2. **Avatar Starts First**: The avatar session is started BEFORE the agent session
3. **Automatic Publishing**: The avatar automatically:
   - Joins the LiveKit room as a separate participant
   - Publishes video and audio tracks
   - Receives audio from the agent for lip-sync
4. **No Manual Video Generation**: Unlike the placeholder, real avatars handle all video rendering on their servers

## Frontend Configuration

The frontend automatically detects and displays video tracks from the avatar. No changes needed!

However, you can set the provider in `frontend/.env` for UI display:
```env
VITE_AVATAR_PROVIDER=tavus  # or 'beyond-presence'
```

## Troubleshooting

### "Tavus plugin not installed"
```bash
pip install 'livekit-agents[tavus]'
```

### "Beyond Presence plugin not installed"
```bash
pip install 'livekit-agents[bey]'
```

### "TAVUS_API_KEY and TAVUS_REPLICA_ID must be set"
- Check your `backend/.env` file
- Make sure variables are set correctly
- Restart the backend agent after changing `.env`

### "BEY_API_KEY and BEY_AVATAR_ID must be set"
- Check your `backend/.env` file
- Use `BEY_API_KEY` and `BEY_AVATAR_ID` (or `BEYOND_PRESENCE_API_KEY` and `BEYOND_PRESENCE_AVATAR_ID`)
- Restart the backend agent

### Avatar not appearing in frontend
1. Check backend logs for "✅ Avatar session started successfully"
2. Check frontend console for video track subscription
3. Verify the avatar participant joined the room (check LiveKit dashboard)

### Audio not syncing with video
- Make sure the avatar session is started BEFORE the agent session
- Check that `AVATAR_PROVIDER` is set correctly
- Verify the avatar is receiving audio from the agent (check logs)

## Performance Benefits

Using real avatars (Tavus/Beyond Presence) vs placeholder:

| Feature | Placeholder | Real Avatar |
|---------|------------|-------------|
| CPU Usage | High (local generation) | Low (server-side) |
| Lag | Possible | Minimal |
| Quality | Test pattern | Hyper-realistic |
| Lip-sync | None | Automatic |
| Setup | Simple | Requires API keys |

## Next Steps

1. **Test with Tavus/Beyond Presence**: Set up credentials and test the integration
2. **Customize Avatar**: Configure your avatar's appearance and behavior in the provider dashboard
3. **Optimize Settings**: Adjust video quality/performance settings if needed

## Support

- **Tavus Docs**: https://docs.livekit.io/agents/integrations/avatar/tavus
- **Beyond Presence Docs**: https://docs.livekit.io/agents/integrations/avatar/bey
- **LiveKit Agents Docs**: https://docs.livekit.io/agents
