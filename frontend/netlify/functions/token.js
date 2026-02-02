// Netlify serverless function for LiveKit token generation
const { AccessToken } = require('livekit-server-sdk')

exports.handler = async (event, context) => {
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      body: JSON.stringify({ error: 'Method not allowed' }),
    }
  }

  try {
    const { room, participant } = JSON.parse(event.body)

    if (!room || !participant) {
      return {
        statusCode: 400,
        body: JSON.stringify({ error: 'Room and participant are required' }),
      }
    }

    const apiKey = process.env.LIVEKIT_API_KEY
    const apiSecret = process.env.LIVEKIT_API_SECRET
    const livekitUrl = process.env.LIVEKIT_URL

    if (!apiKey || !apiSecret || !livekitUrl) {
      return {
        statusCode: 500,
        body: JSON.stringify({ error: 'LiveKit configuration missing' }),
      }
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

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        token,
        url: livekitUrl,
      }),
    }
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: error.message }),
    }
  }
}
