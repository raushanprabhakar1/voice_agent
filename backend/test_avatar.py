#!/usr/bin/env python3
"""
Quick test script to verify avatar setup
"""
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("Avatar Configuration Check")
print("=" * 60)

# Check environment variables
enable_avatar = os.getenv("ENABLE_AVATAR_VIDEO", "false").lower() == "true"
avatar_provider = os.getenv("AVATAR_PROVIDER", "").lower()

print(f"\n1. ENABLE_AVATAR_VIDEO: {enable_avatar}")
print(f"2. AVATAR_PROVIDER: {avatar_provider or '(not set)'}")

if enable_avatar:
    print("\n✅ Avatar video is ENABLED")
    
    if avatar_provider == "placeholder":
        print("✅ Using placeholder/test pattern video")
        print("\nThis should work immediately - no additional setup needed!")
        
    elif avatar_provider == "tavus":
        print("\n🔧 Tavus Configuration:")
        tavus_key = os.getenv("TAVUS_API_KEY")
        replica_id = os.getenv("TAVUS_REPLICA_ID")
        persona_id = os.getenv("TAVUS_PERSONA_ID")
        
        print(f"  TAVUS_API_KEY: {'✅ Set' if tavus_key else '❌ NOT SET'}")
        print(f"  TAVUS_REPLICA_ID: {'✅ Set' if replica_id else '❌ NOT SET'}")
        print(f"  TAVUS_PERSONA_ID: {'✅ Set' if persona_id else '⚠️  Optional'}")
        
        if not tavus_key or not replica_id:
            print("\n❌ Missing required Tavus credentials!")
            print("   Set TAVUS_API_KEY and TAVUS_REPLICA_ID in .env")
        else:
            # Check if plugin is installed
            try:
                from livekit.plugins import tavus
                print("  ✅ Tavus plugin is installed")
            except ImportError:
                print("  ❌ Tavus plugin NOT installed")
                print("   Install with: pip install 'livekit-agents[tavus]'")
                
    elif avatar_provider == "beyond-presence":
        print("\n🔧 Beyond Presence Configuration:")
        api_key = os.getenv("BEYOND_PRESENCE_API_KEY")
        avatar_id = os.getenv("BEYOND_PRESENCE_AVATAR_ID")
        
        print(f"  BEYOND_PRESENCE_API_KEY: {'✅ Set' if api_key else '❌ NOT SET'}")
        print(f"  BEYOND_PRESENCE_AVATAR_ID: {'✅ Set' if avatar_id else '❌ NOT SET'}")
        
        if not api_key or not avatar_id:
            print("\n❌ Missing required Beyond Presence credentials!")
        else:
            try:
                from livekit.plugins import beyond_presence
                print("  ✅ Beyond Presence plugin is installed")
            except ImportError:
                print("  ❌ Beyond Presence plugin NOT installed")
                print("   Install with: pip install 'livekit-agents[beyond-presence]'")
    else:
        print(f"\n⚠️  Unknown provider: {avatar_provider}")
        print("   Valid options: 'placeholder', 'tavus', 'beyond-presence'")
else:
    print("\n❌ Avatar video is DISABLED")
    print("   Set ENABLE_AVATAR_VIDEO=true in .env to enable")

print("\n" + "=" * 60)
print("Frontend Configuration")
print("=" * 60)

print("\nMake sure frontend/.env has:")
print("  VITE_AVATAR_PROVIDER=livekit-video")

print("\n" + "=" * 60)
print("Quick Start (Placeholder Video)")
print("=" * 60)
print("""
1. Set in backend/.env:
   ENABLE_AVATAR_VIDEO=true
   AVATAR_PROVIDER=placeholder

2. Set in frontend/.env:
   VITE_AVATAR_PROVIDER=livekit-video

3. Restart backend agent

4. Connect from frontend - you should see animated test pattern
""")
