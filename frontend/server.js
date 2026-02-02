// Simple Express server for local development token generation
const express = require('express')
const cors = require('cors')
const { AccessToken, RoomServiceClient, AgentDispatchClient } = require('livekit-server-sdk')
require('dotenv').config()

const app = express()
app.use(cors())
app.use(express.json())

app.post('/api/token', async (req, res) => {
  try {
    const { room, participant } = req.body

    if (!room || !participant) {
      return res.status(400).json({ error: 'Room and participant are required' })
    }

    const apiKey = process.env.LIVEKIT_API_KEY
    const apiSecret = process.env.LIVEKIT_API_SECRET
    const livekitUrl = process.env.LIVEKIT_URL

    if (!apiKey || !apiSecret || !livekitUrl) {
      return res.status(500).json({ 
        error: 'LiveKit configuration missing. Please set LIVEKIT_API_KEY, LIVEKIT_API_SECRET, and LIVEKIT_URL in your .env file' 
      })
    }

    const at = new AccessToken(apiKey, apiSecret, {
      identity: participant,
    })

    at.addGrant({
      room: room,
      roomJoin: true,
      canPublish: true,
      canSubscribe: true,
      canPublishData: true,
    })

    const token = await at.toJwt()

    // Ensure the room exists and explicitly dispatch the agent
    try {
      const roomService = new RoomServiceClient(livekitUrl, apiKey, apiSecret)
      
      // Create or get the room
      await roomService.createRoom({
        name: room,
        emptyTimeout: 300, // 5 minutes
        maxParticipants: 10,
      })
      
      console.log(`Room ready: ${room}`)
      
      // Explicitly dispatch the agent to this room
      // This is required for LiveKit Cloud - agent must have a name for explicit dispatch
      try {
        const agentDispatch = new AgentDispatchClient(livekitUrl, apiKey, apiSecret)
        
        // Dispatch agent with explicit name (must match backend agent_name)
        const dispatch = await agentDispatch.createDispatch(room, "voice-agent", {
          metadata: JSON.stringify({ participant: participant })
        })
        
        console.log(`✅ Agent dispatched to room: ${room}`)
        console.log(`   Dispatch ID: ${dispatch.id}`)
        console.log(`   Agent name: voice-agent`)
      } catch (dispatchError) {
        console.error(`❌ Failed to dispatch agent: ${dispatchError.message}`)
        // Continue anyway - log the error but don't fail the token generation
      }
    } catch (roomError) {
      // Room might already exist, that's okay
      console.log(`Room note: ${roomError.message}`)
    }

    return res.status(200).json({
      token,
      url: livekitUrl,
    })
  } catch (error) {
    console.error('Token generation error:', error)
    return res.status(500).json({ error: error.message })
  }
})

const PORT = process.env.PORT || 3001
app.listen(PORT, () => {
  console.log(`Token server running on http://localhost:${PORT}`)
})
