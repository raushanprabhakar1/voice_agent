#!/usr/bin/env python3
"""
Quick diagnostic script to check if the agent can start
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("Agent Diagnostic Check")
print("=" * 60)

# Check Python version
print(f"\nPython version: {sys.version}")

# Check imports
print("\nChecking imports...")
try:
    from livekit import agents, rtc
    print("  ✓ livekit imported")
except Exception as e:
    print(f"  ✗ Failed to import livekit: {e}")
    sys.exit(1)

try:
    from livekit.agents import cli, JobContext, WorkerOptions, llm
    print("  ✓ livekit.agents imported")
except Exception as e:
    print(f"  ✗ Failed to import livekit.agents: {e}")
    sys.exit(1)

try:
    from livekit.plugins import deepgram, cartesia
    print("  ✓ livekit.plugins imported")
except Exception as e:
    print(f"  ✗ Failed to import livekit.plugins: {e}")
    sys.exit(1)

try:
    from database import Database
    print("  ✓ database imported")
except Exception as e:
    print(f"  ✗ Failed to import database: {e}")
    sys.exit(1)

try:
    from tools import AppointmentTools
    print("  ✓ tools imported")
except Exception as e:
    print(f"  ✗ Failed to import tools: {e}")
    sys.exit(1)

# Check environment variables
print("\nChecking environment variables...")
required = {
    "LIVEKIT_URL": os.getenv("LIVEKIT_URL"),
    "LIVEKIT_API_KEY": os.getenv("LIVEKIT_API_KEY"),
    "LIVEKIT_API_SECRET": os.getenv("LIVEKIT_API_SECRET"),
    "DEEPGRAM_API_KEY": os.getenv("DEEPGRAM_API_KEY"),
    "CARTESIA_API_KEY": os.getenv("CARTESIA_API_KEY"),
    "SUPABASE_URL": os.getenv("SUPABASE_URL"),
    "SUPABASE_KEY": os.getenv("SUPABASE_KEY"),
}

all_set = True
for key, value in required.items():
    if value:
        print(f"  ✓ {key}: {'*' * min(len(value), 10)}")
    else:
        print(f"  ✗ {key}: NOT SET")
        all_set = False

if not all_set:
    print("\n⚠️  Some required environment variables are not set!")
    print("   Make sure your .env file is configured correctly.")
else:
    print("\n✓ All required environment variables are set")

# Check LLM provider
print(f"\nLLM Provider: {os.getenv('LLM_PROVIDER', 'NOT SET')}")
print(f"LLM Model: {os.getenv('LLM_MODEL', 'NOT SET')}")

print("\n" + "=" * 60)
print("Diagnostic complete!")
print("=" * 60)
print("\nIf all checks passed, try running: python agent.py dev")
print("You should see logs immediately when the agent starts.")
