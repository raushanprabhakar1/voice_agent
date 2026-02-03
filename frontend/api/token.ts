// Vercel serverless function for LiveKit token generation
import type { VercelRequest, VercelResponse } from '@vercel/node'
import { AccessToken } from 'livekit-server-sdk'

export default async function handler(
  req: VercelRequest,
  res: VercelResponse
) {
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

  const apiKey = process.env.LIVEKIT_API_KEY
  const apiSecret = process.env.LIVEKIT_API_SECRET
  const livekitUrl = process.env.LIVEKIT_URL

  // Provide detailed error message about which variables are missing
  const missingVars: string[] = []
  if (!apiKey) missingVars.push('LIVEKIT_API_KEY')
  if (!apiSecret) missingVars.push('LIVEKIT_API_SECRET')
  if (!livekitUrl) missingVars.push('LIVEKIT_URL')

  if (missingVars.length > 0) {
    console.error('❌ Missing environment variables:', missingVars.join(', '))
    return res.status(500).json({ 
      error: `LiveKit configuration missing: ${missingVars.join(', ')}. Please set these environment variables in your Vercel deployment settings.` 
    })
  }

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

    return res.status(200).json({
      token,
      url: livekitUrl,
    })
  } catch (error: any) {
    console.error('❌ Error generating token:', error)
    return res.status(500).json({ 
      error: `Failed to generate token: ${error.message || 'Unknown error'}` 
    })
  }
}
