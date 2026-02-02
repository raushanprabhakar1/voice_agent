# Why There Are 3 Participants

## Expected Participants

When using Beyond Presence avatar, you will see **3 participants** in the room:

1. **User** (`user-...`) - The person using the web app
2. **Main Agent** (`agent-AJ_...`) - Your voice agent that handles conversation
3. **Beyond Presence Avatar** (`bey-avatar-agent`) - The avatar that displays video

## Why 3 Participants?

This is **correct behavior** when using Beyond Presence:

- The **main agent** handles:
  - Speech-to-text (listening to user)
  - LLM (understanding and responding)
  - Text-to-speech (generating audio)
  - Tool execution (booking appointments, etc.)

- The **avatar participant** handles:
  - Video rendering (displaying the avatar)
  - Audio/video synchronization (lip-sync)
  - Publishing video tracks to the room

They work together:
1. Main agent generates audio response
2. Audio is sent to avatar participant
3. Avatar participant renders video with lip-sync
4. Avatar publishes video track to room
5. Frontend displays the video

## If You See Duplicate Connections

If you see **multiple** "Participant connected: bey-avatar-agent" messages, this indicates:

1. **Multiple agent processes running** - Check if you have multiple backend processes
2. **Avatar retrying connection** - Beyond Presence might be retrying after errors
3. **Multiple rooms** - Each room gets its own avatar participant

## To Verify

Check your backend logs for:
- How many times `entrypoint` is called
- How many job requests are received
- If there are multiple agent processes

## If You Want Only 2 Participants

If you don't want the avatar participant, you can:

1. **Disable avatar**: Set `AVATAR_PROVIDER=placeholder` or remove it
2. **Use placeholder video**: Set `ENABLE_AVATAR_VIDEO=true` and `AVATAR_PROVIDER=placeholder`

This will give you:
- User participant
- Main agent participant
- (No separate avatar participant - agent publishes video directly)

## Summary

**3 participants is normal** when using Beyond Presence. The avatar needs to be a separate participant to handle video rendering and synchronization.

If you see **more than 3** participants, or **duplicate avatar connections**, that's when you should investigate.
