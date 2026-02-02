# SuperBryn Voice Agent - Frontend

React frontend for the AI voice agent using LiveKit Web SDK.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create a `.env` file:
```env
# LiveKit Configuration (for token server)
LIVEKIT_URL=wss://your-livekit-server.com
LIVEKIT_API_KEY=your-api-key
LIVEKIT_API_SECRET=your-api-secret

# Frontend (Vite)
VITE_LIVEKIT_URL=wss://your-livekit-server.com
```

3. For local development, you need to run the token server:
   - In one terminal, start the token server:
     ```bash
     npm run dev:token
     ```
   - In another terminal, start the frontend:
     ```bash
     npm run dev
     ```

4. For production deployment:
   - For Vercel: Use `api/token.ts` as a serverless function
   - For Netlify: Use `netlify/functions/token.js`

5. Build for production:
```bash
npm run build
```

## Deployment

### Vercel
1. Connect your GitHub repo
2. Set environment variables in Vercel dashboard
3. Deploy

### Netlify
1. Connect your GitHub repo
2. Set build command: `npm run build`
3. Set publish directory: `dist`
4. Set environment variables
5. Deploy

## Avatar Integration

To integrate Beyond Presence or Tavus:

1. Replace the placeholder avatar in `VoiceAgent.tsx`
2. Use their SDK to sync avatar with audio
3. Update the avatar URL/component accordingly

Example for Tavus:
```typescript
import { Tavus } from '@tavus/react'

// In VoiceAgent component
<Tavus
  replicaId="your-replica-id"
  audioTrack={audioTrack}
/>
```
