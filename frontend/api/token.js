// Vercel serverless function for LiveKit token generation
const { AccessToken, RoomServiceClient, AgentDispatchClient } = require('livekit-server-sdk')

module.exports = async function handler(req, res) {
  try {
    // Enable CORS
    res.setHeader('Access-Control-Allow-Origin', '*')
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS')
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type')

    if (req.method === 'OPTIONS') {
      return res.status(200).end()
    }

    if (req.method !== 'POST') {
      return res.status(405).json({ error: 'Method not allowed' })
    }

    const { room, participant } = req.body

    if (!room || !participant) {
      return res.status(400).json({ error: 'Room and participant are required' })
    }

    // Check environment variables
    const apiKey = process.env.LIVEKIT_API_KEY
    const apiSecret = process.env.LIVEKIT_API_SECRET
    const livekitUrl = process.env.LIVEKIT_URL

    // Debug: Log which variables are present (without logging values)
    console.log('🔍 Environment check:', {
      hasApiKey: !!apiKey,
      hasApiSecret: !!apiSecret,
      hasLivekitUrl: !!livekitUrl,
      apiKeyLength: apiKey?.length || 0,
      apiSecretLength: apiSecret?.length || 0,
      livekitUrlLength: livekitUrl?.length || 0,
    })

    // Provide detailed error message about which variables are missing
    const missingVars = []
    if (!apiKey || apiKey.trim() === '') missingVars.push('LIVEKIT_API_KEY')
    if (!apiSecret || apiSecret.trim() === '') missingVars.push('LIVEKIT_API_SECRET')
    if (!livekitUrl || livekitUrl.trim() === '') missingVars.push('LIVEKIT_URL')

    if (missingVars.length > 0) {
      console.error('❌ Missing environment variables:', missingVars.join(', '))
      console.error('❌ Available env vars:', Object.keys(process.env).filter(k => k.includes('LIVEKIT')))
      return res.status(500).json({ 
        error: `LiveKit configuration missing: ${missingVars.join(', ')}. Please set these environment variables in your Vercel deployment settings (Settings → Environment Variables). Make sure they are set for the correct environment (Production/Preview/Development) and redeploy.` 
      })
    }

    // Validate API key and secret format
    if (apiKey && apiKey.length < 10) {
      console.error('❌ LIVEKIT_API_KEY appears to be invalid (too short)')
      return res.status(500).json({ 
        error: 'LIVEKIT_API_KEY appears to be invalid. Please check your Vercel environment variables.' 
      })
    }

    if (apiSecret && apiSecret.length < 20) {
      console.error('❌ LIVEKIT_API_SECRET appears to be invalid (too short)')
      return res.status(500).json({ 
        error: 'LIVEKIT_API_SECRET appears to be invalid. Please check your Vercel environment variables.' 
      })
    }

    // Generate token
    try {
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
      // This is required for LiveKit Cloud - agent must be dispatched explicitly
      try {
        const roomService = new RoomServiceClient(livekitUrl, apiKey, apiSecret)
        
        // Create or get the room
        await roomService.createRoom({
          name: room,
          emptyTimeout: 300, // 5 minutes
          maxParticipants: 10,
        })
        
        console.log(`✅ Room ready: ${room}`)
        
        // Explicitly dispatch the agent to this room
        // The agent name "voice-agent" must match the backend agent_name
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
          // The agent might still connect via other means
        }
      } catch (roomError) {
        // Room might already exist, that's okay
        console.log(`⚠️ Room creation note: ${roomError.message}`)
        // Try to dispatch anyway
        try {
          const agentDispatch = new AgentDispatchClient(livekitUrl, apiKey, apiSecret)
          const dispatch = await agentDispatch.createDispatch(room, "voice-agent", {
            metadata: JSON.stringify({ participant: participant })
          })
          console.log(`✅ Agent dispatched to existing room: ${room}`)
        } catch (dispatchError) {
          console.error(`❌ Failed to dispatch agent to existing room: ${dispatchError.message}`)
        }
      }

      console.log('✅ Token generated successfully')
      return res.status(200).json({
        token,
        url: livekitUrl,
      })
    } catch (tokenError) {
      console.error('❌ Error generating token:', tokenError)
      console.error('❌ Token error details:', {
        message: tokenError.message,
        stack: tokenError.stack,
        name: tokenError.name,
      })
      return res.status(500).json({ 
        error: `Failed to generate token: ${tokenError.message || 'Unknown error'}. Please verify your LIVEKIT_API_KEY and LIVEKIT_API_SECRET are correct.` 
      })
    }
  } catch (error) {
    // Catch any unexpected errors
    console.error('❌ Unexpected error in token handler:', error)
    console.error('❌ Error details:', {
      message: error.message,
      stack: error.stack,
      name: error.name,
    })
    return res.status(500).json({ 
      error: `Server error: ${error.message || 'Unknown error'}. Check Vercel function logs for details.` 
    })
  }
}
