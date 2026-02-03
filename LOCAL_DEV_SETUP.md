# Local Development Setup

## Overview

For local development, you need to run two servers:
1. **Frontend dev server** (Vite) - port 3000
2. **Token server** (Express) - port 3001

## Setup

### Step 1: Install Dependencies

```bash
cd frontend
npm install
```

### Step 2: Set Up Environment Variables

Create `frontend/.env` file:

```env
# LiveKit Configuration
LIVEKIT_URL=wss://your-livekit-server.com
LIVEKIT_API_KEY=your-api-key
LIVEKIT_API_SECRET=your-api-secret

# Frontend (Vite)
VITE_LIVEKIT_URL=wss://your-livekit-server.com
VITE_AVATAR_PROVIDER=livekit-video
```

### Step 3: Start Token Server

In one terminal:

```bash
cd frontend
npm run dev:token
```

You should see:
```
Token server running on http://localhost:3001
```

### Step 4: Start Frontend Dev Server

In another terminal:

```bash
cd frontend
npm run dev
```

You should see:
```
VITE v5.x.x  ready in xxx ms
➜  Local:   http://localhost:3000/
```

### Step 5: Open Browser

Open `http://localhost:3000` in your browser.

## How It Works

### Development Mode

- **Frontend**: Runs on `http://localhost:3000` (Vite)
- **Token Server**: Runs on `http://localhost:3001` (Express)
- **Vite Proxy**: Automatically proxies `/api/*` requests to `http://localhost:3001`
- **Frontend Code**: Uses `http://localhost:3001/api/token` directly in dev mode

### Production Mode (Vercel)

- **Frontend**: Deployed to Vercel
- **Token API**: `api/token.ts` at project root becomes Vercel serverless function
- **Frontend Code**: Uses `/api/token` (relative URL, handled by Vercel)

## File Structure

```
submission/
├── api/
│   └── token.ts          # Vercel serverless function (production)
├── frontend/
│   ├── server.js         # Local token server (development)
│   ├── vite.config.ts    # Vite config with proxy
│   └── src/
│       └── App.tsx        # Uses tokenUrl based on dev/prod mode
```

## Troubleshooting

### Token Server Not Starting

**Error**: `Port 3001 already in use`

**Solution**:
```bash
# Kill process on port 3001
lsof -ti:3001 | xargs kill -9

# Or change port in server.js
const PORT = process.env.PORT || 3002
```

### Frontend Can't Reach Token Server

**Error**: `Failed to reach token API`

**Solution**:
1. Make sure token server is running (`npm run dev:token`)
2. Check that token server is on port 3001
3. Check browser console for CORS errors
4. Verify `vite.config.ts` has proxy configuration

### Environment Variables Not Working

**Error**: `LiveKit configuration missing`

**Solution**:
1. Create `frontend/.env` file
2. Add `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`
3. Restart token server after adding variables

## Quick Start Commands

```bash
# Terminal 1: Token Server
cd frontend
npm run dev:token

# Terminal 2: Frontend Dev Server
cd frontend
npm run dev

# Terminal 3: Backend Agent (if testing locally)
cd backend
python agent.py
```

## Production vs Development

| Aspect | Development | Production |
|--------|------------|------------|
| Token Server | `server.js` on port 3001 | Vercel serverless function |
| Token URL | `http://localhost:3001/api/token` | `/api/token` |
| Frontend | `http://localhost:3000` | Vercel URL |
| Backend | Local or Railway | Railway |

## Notes

- The frontend automatically detects dev mode using `import.meta.env.DEV`
- In dev mode, it uses `http://localhost:3001/api/token`
- In production, it uses `/api/token` (Vercel handles routing)
- Vite proxy is configured but not needed since we use direct URL in dev mode
