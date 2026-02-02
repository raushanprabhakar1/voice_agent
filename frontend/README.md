# Frontend - SuperBryn Voice Agent

React frontend for the AI voice agent using LiveKit Web SDK and Vite.

## 🏗️ Architecture

- **React 18**: UI framework
- **TypeScript**: Type safety
- **Vite**: Build tool and dev server
- **LiveKit Web SDK**: Real-time communication
- **Tailwind CSS**: Styling (via CSS modules)

## 📦 Installation

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Set up environment variables**:
   Create a `.env` file:
   ```env
   VITE_LIVEKIT_URL=wss://your-livekit-server.com
   VITE_AVATAR_PROVIDER=livekit-video
   ```

3. **For local development with token server**:
   ```env
   # Add these for token API (if running locally)
   LIVEKIT_URL=wss://your-livekit-server.com
   LIVEKIT_API_KEY=your-api-key
   LIVEKIT_API_SECRET=your-api-secret
   ```

## 🚀 Running

### Development Mode

```bash
npm run dev
```

The app will be available at `http://localhost:5173`

### Production Build

```bash
npm run build
```

Output will be in the `dist` directory.

### Preview Production Build

```bash
npm run preview
```

## 📁 File Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── VoiceAgent.tsx         # Main voice agent UI
│   │   ├── AvatarPlayer.tsx       # Avatar rendering component
│   │   ├── ToolCallDisplay.tsx    # Tool call visualization
│   │   └── ConversationSummary.tsx # Summary display
│   ├── App.tsx                     # Main app component
│   ├── main.tsx                    # Entry point
│   └── index.css                   # Global styles
├── api/
│   └── token.ts                   # Vercel serverless function
├── netlify/
│   └── functions/
│       └── token.js                # Netlify serverless function
├── public/                         # Static assets
├── package.json
├── vite.config.ts
├── vercel.json                     # Vercel configuration
└── netlify.toml                    # Netlify configuration
```

## 🎨 Components

### App.tsx
Main application component that:
- Handles LiveKit room connection
- Manages tool calls state
- Displays conversation summary
- Handles microphone permissions

### VoiceAgent.tsx
Voice agent component that:
- Manages audio/video tracks
- Handles speaking detection
- Displays avatar
- Provides mute/unmute controls

### AvatarPlayer.tsx
Avatar rendering component that:
- Handles LiveKit video tracks
- Supports multiple avatar providers
- Shows loading/error states
- Syncs with speaking indicator

### ToolCallDisplay.tsx
Tool call visualization component that:
- Displays all tool calls in real-time
- Shows tool name, arguments, and results
- Provides expandable details
- Highlights new tool calls
- Shows execution status (pending/success/error)

### ConversationSummary.tsx
Summary display component that:
- Shows conversation summary
- Lists all tool calls made
- Displays key points and preferences
- Formats data in a user-friendly way

## 🔧 Configuration

### Environment Variables

**Frontend (VITE_ prefix)**:
```env
VITE_LIVEKIT_URL=wss://your-livekit-server.com
VITE_AVATAR_PROVIDER=livekit-video  # or tavus, beyond-presence, none
```

**Token API (for serverless functions)**:
```env
LIVEKIT_URL=wss://your-livekit-server.com
LIVEKIT_API_KEY=your-api-key
LIVEKIT_API_SECRET=your-api-secret
```

### Avatar Providers

The frontend supports multiple avatar providers:

- **`livekit-video`**: LiveKit video tracks (default)
- **`tavus`**: Tavus avatar (requires Tavus SDK)
- **`beyond-presence`**: Beyond Presence avatar (requires Beyond Presence SDK)
- **`none`**: No avatar (placeholder)

## 🔌 Token API

The frontend needs a token server to generate LiveKit access tokens.

### Vercel (Automatic)

The `api/token.ts` file is automatically converted to a Vercel serverless function:
- Endpoint: `https://your-app.vercel.app/api/token`
- Method: POST
- Body: `{ room: string, participant: string }`
- Returns: `{ token: string, url: string }`

### Netlify (Automatic)

The `netlify/functions/token.js` file is automatically deployed:
- Endpoint: `https://your-app.netlify.app/.netlify/functions/token`
- Method: POST
- Body: `{ room: string, participant: string }`
- Returns: `{ token: string, url: string }`

### Local Development

For local development, you can:
1. Use the token server in `server.js`:
   ```bash
   node server.js
   ```
2. Or use a separate token server
3. Update `App.tsx` to point to your local token server

## 📡 Data Channels

The frontend receives tool calls and conversation summaries via LiveKit data channels:

- **Tool Calls**: Real-time updates when agent executes tools
- **Tool Results**: Results of tool executions
- **Conversation Summary**: Summary sent at end of conversation

All data is sent with `reliable: true` to ensure delivery.

## 🎨 Styling

The app uses CSS modules for component-specific styles:
- `App.css`: Main app styles
- `VoiceAgent.css`: Voice agent component styles
- `AvatarPlayer.css`: Avatar component styles
- `ToolCallDisplay.css`: Tool call display styles
- `ConversationSummary.css`: Summary display styles

## 🧪 Testing

### Local Testing

1. Start the backend agent
2. Start the frontend dev server: `npm run dev`
3. Open `http://localhost:5173`
4. Click "Start Voice Call"
5. Test the complete flow

### Production Testing

1. Deploy frontend to Vercel/Netlify
2. Visit deployed URL
3. Test all features
4. Check browser console for errors

## 🚢 Deployment

For detailed deployment instructions, see the main [DEPLOY_STEP_BY_STEP.md](../DEPLOY_STEP_BY_STEP.md).

### Quick Deployment (Vercel)

1. Connect GitHub repo to Vercel
2. Set root directory: `frontend`
3. Set build command: `npm run build`
4. Set output directory: `dist`
5. Add environment variables
6. Deploy

### Quick Deployment (Netlify)

1. Connect GitHub repo to Netlify
2. Set base directory: `frontend`
3. Set build command: `npm run build`
4. Set publish directory: `frontend/dist`
5. Add environment variables
6. Deploy

## 🔍 Features

### Real-time Tool Call Display

- Shows all tool calls as they happen
- Displays tool name, arguments, and results
- Expandable details for each call
- Status indicators (pending/success/error)
- Auto-scrolls to new calls
- Highlights new calls

### Conversation Summary

- Displays at end of conversation
- Shows all tool calls made
- Lists key points and preferences
- User-friendly formatting

### Avatar Display

- Supports LiveKit video tracks
- Ready for Tavus/Beyond Presence integration
- Shows speaking indicator
- Loading and error states

### Microphone Management

- Requests permission on start
- Shows clear error messages if denied
- Mute/unmute controls
- Visual feedback

## 🔧 Troubleshooting

### Token API Not Working

- Verify `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET` are set
- Check token endpoint is accessible
- Verify CORS is configured (if using separate server)
- Check browser console for errors

### Can't Connect to Room

- Verify `VITE_LIVEKIT_URL` is set correctly
- Check token API returns valid token
- Verify backend agent is running
- Check browser console for connection errors

### Tool Calls Not Showing

- Check data channel is connected
- Verify backend is sending tool call data
- Check browser console for data channel errors
- Verify `ToolCallDisplay` component is rendering

### Avatar Not Showing

- Verify `VITE_AVATAR_PROVIDER` is set
- Check backend is publishing video tracks
- Verify video track subscription works
- Check browser console for video errors

### Microphone Permission Denied

- Check browser settings
- Clear site permissions
- Try different browser
- Check browser console for permission errors
