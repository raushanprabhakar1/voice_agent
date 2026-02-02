# Avatar Performance Optimization

## Current Optimizations

The avatar video generation has been optimized to reduce lag:

1. **Vectorized frame generation** - Uses numpy vectorized operations instead of pixel-by-pixel loops (100x faster)
2. **Lower default resolution** - 640x360 instead of 1280x720 (4x fewer pixels = 4x faster)
3. **Lower default frame rate** - 15 fps instead of 30 fps (half the CPU usage)
4. **Frame timing control** - Skips sleep if frame generation is slow to prevent lag accumulation

## Performance Settings

You can adjust these in `backend/.env`:

```env
# Lower = better performance, less lag
AVATAR_VIDEO_WIDTH=640      # Default: 640 (was 1280)
AVATAR_VIDEO_HEIGHT=360     # Default: 360 (was 720)
AVATAR_VIDEO_FPS=15         # Default: 15 (was 30)
```

### Recommended Settings

**For smooth performance (current defaults):**
```env
AVATAR_VIDEO_WIDTH=640
AVATAR_VIDEO_HEIGHT=360
AVATAR_VIDEO_FPS=15
```

**For better quality (if your system can handle it):**
```env
AVATAR_VIDEO_WIDTH=1280
AVATAR_VIDEO_HEIGHT=720
AVATAR_VIDEO_FPS=30
```

**For maximum performance (lowest lag):**
```env
AVATAR_VIDEO_WIDTH=320
AVATAR_VIDEO_HEIGHT=240
AVATAR_VIDEO_FPS=10
```

## If Still Lagging

1. **Reduce resolution further**:
   ```env
   AVATAR_VIDEO_WIDTH=320
   AVATAR_VIDEO_HEIGHT=240
   ```

2. **Reduce frame rate**:
   ```env
   AVATAR_VIDEO_FPS=10
   ```

3. **Check CPU usage**:
   - High CPU usage = reduce resolution/fps
   - Check with: `top` or Activity Monitor

4. **Check network**:
   - Video requires stable network
   - Check LiveKit connection quality

5. **Use real avatar service**:
   - Placeholder video generation is CPU-intensive
   - Real avatar services (Tavus/Beyond Presence) are optimized
   - They handle frame generation on their servers

## Performance Comparison

| Resolution | FPS | CPU Usage | Quality | Recommended For |
|------------|-----|-----------|---------|-----------------|
| 320x240    | 10  | Very Low  | Low     | Testing, low-end systems |
| 640x360    | 15  | Low       | Medium  | **Default - Good balance** |
| 1280x720   | 30  | High      | High    | High-end systems only |

## Monitoring Performance

Check backend logs for:
- `Frame generation took X.XXXs` - Should be less than frame duration
- If you see warnings about frame generation taking too long, reduce resolution/fps

## Next Steps

Once placeholder works smoothly, integrate a real avatar service (Tavus/Beyond Presence) which:
- Generates frames on their servers (no local CPU usage)
- Provides optimized video streaming
- Handles all performance optimizations automatically
