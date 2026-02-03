// Vercel serverless function for LiveKit token generation
import type { VercelRequest, VercelResponse } from '@vercel/node'
import { AccessToken } from 'livekit-server-sdk'

export default async function handler(
  req: VercelRequest,
  res: VercelResponse
) {
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

  if (!apiKey || !apiSecret || !livekitUrl) {
    return res.status(500).json({ error: 'LiveKit configuration missing' })
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

  return res.status(200).json({
    token,
    url: livekitUrl,
  })
}
