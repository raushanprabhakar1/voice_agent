# Railway Deployment Fix

## Issue

Railway error:
```
/app/.venv/bin/python: No module named livekit.agents.__main__; 'livekit.agents' is a package and cannot be directly executed
```

## Solution

The correct start command for Railway is:

```
python agent.py
```

**NOT** `python -m livekit.agents dev agent.py`

## Steps to Fix

1. Go to your Railway project dashboard
2. Click on your service
3. Go to "Settings" tab
4. Scroll to "Deploy" section
5. Find "Start Command"
6. Change it from:
   ```
   python -m livekit.agents dev agent.py
   ```
   To:
   ```
   python agent.py
   ```
7. Save changes
8. Railway will automatically redeploy

## Why This Works

The `agent.py` file has a `if __name__ == "__main__"` block that uses `cli.run_app()` from LiveKit Agents. This means it can be run directly with `python agent.py` without needing the `-m livekit.agents` module execution.

## Alternative Commands

If `python agent.py` doesn't work, try:

1. **Using livekit-agents CLI** (if installed):
   ```
   livekit-agents dev agent.py
   ```

2. **Using python3 explicitly**:
   ```
   python3 agent.py
   ```

3. **With full path** (if needed):
   ```
   /app/.venv/bin/python agent.py
   ```

## Verification

After updating the command, check the Railway logs. You should see:
- ✅ "Starting LiveKit agent worker..."
- ✅ "Agent will listen for new connections on LiveKit server"
- ✅ "registered_workers" (when agent connects to LiveKit)

If you still see errors, check:
- All environment variables are set correctly
- `livekit-agents` package is installed (in requirements.txt)
- Python version is 3.9+ (Railway should auto-detect)
