# Implementation Notes

## Architecture Overview

### Backend (Python)
- **LiveKit Agents**: Voice pipeline agent framework
- **Deepgram**: Speech-to-text (STT)
- **Cartesia**: Text-to-speech (TTS)
- **LLM**: OpenAI/Claude/Together/OpenRouter for conversation
- **Supabase**: Database for persistence

### Frontend (React + TypeScript)
- **LiveKit Web SDK**: Real-time communication
- **React**: UI framework
- **Vite**: Build tool

## Key Implementation Details

### Tool Integration
Tools are registered with the LLM instance using `llm_instance.add_tool()`. The `on_tool_calls()` method is overridden to:
1. Execute the tool
2. Track tool calls for summary
3. Send tool call info to frontend via data channel
4. Update user state when needed

### Data Channel Communication
The backend sends three types of messages via LiveKit data channels:
1. `tool_call`: When a tool is invoked
2. `tool_result`: When a tool execution completes
3. `conversation_summary`: When the conversation ends

### Avatar Integration
Currently uses a placeholder avatar. To integrate Tavus or Beyond Presence:
1. Install their SDK
2. Replace the avatar component in `VoiceAgent.tsx`
3. Sync with audio track from LiveKit

### Conversation Summary
Generated at the end of the conversation using the LLM. Includes:
- Summary text
- Appointments booked/cancelled/modified
- User preferences
- Key points
- Tool calls made

## Known Limitations & Future Improvements

1. **Avatar**: Placeholder only - needs Tavus/Beyond Presence integration
2. **Slots**: Hardcoded slots (9 AM, 11 AM, 2 PM, 4 PM for 7 days)
3. **Error Recovery**: Some edge cases may need better handling
4. **Cost Tracking**: Optional bonus feature not implemented
5. **Multi-language**: Currently English only
6. **Audio Quality**: Depends on Cartesia/Deepgram settings

## Testing Checklist

- [x] Voice recognition works
- [x] Agent responds with voice
- [x] Tool calls execute correctly
- [x] Tool calls display in UI
- [x] Appointments can be booked
- [x] Appointments can be retrieved
- [x] Appointments can be cancelled
- [x] Appointments can be modified
- [x] Summary generates at end
- [x] Summary displays in UI
- [x] Database persistence works
- [ ] Avatar syncs with voice (placeholder works)
- [ ] Double-booking prevention works
- [ ] Error handling for edge cases

## Performance Considerations

- **Latency**: Target <3s for responses, <5s for tool calls
- **Database**: Using Supabase for fast queries
- **Audio**: Streaming for real-time conversation
- **Summary**: Generated within 10 seconds of call end

## Security Considerations

- API keys stored in environment variables
- Supabase uses row-level security (can be configured)
- LiveKit tokens generated server-side
- No sensitive data in frontend code

## Deployment Notes

### Backend
- Requires persistent connection (not serverless)
- Use process manager (PM2, supervisor)
- Monitor for crashes and restart

### Frontend
- Static site, can be CDN-hosted
- Token API must be serverless function
- Environment variables set in platform

### Database
- Supabase handles scaling
- Consider indexes for large datasets
- Backup strategy recommended
