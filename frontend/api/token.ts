// Vercel serverless function for LiveKit token generation
import type { VercelRequest, VercelResponse } from '@vercel/node'
import { AccessToken } from 'livekit-server-sdk'

export default async function handler(
  req: VercelRequest,
  res: VercelResponse
) {
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
    const missingVars: string[] = []
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

    // TypeScript: At this point we know these are defined (checked above)
    if (!apiKey || !apiSecret || !livekitUrl) {
      return res.status(500).json({ 
        error: 'Environment variables validation failed unexpectedly.' 
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

      console.log('✅ Token generated successfully')
      return res.status(200).json({
        token,
        url: livekitUrl,
      })
    } catch (tokenError: any) {
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
  } catch (error: any) {
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
