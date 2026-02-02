"""
Avatar integration using LiveKit's built-in avatar support or direct API integration.

This module provides integration with Tavus and Beyond Presence avatars.
"""

import os
import asyncio
import logging
from typing import Optional
from livekit import rtc
from livekit.agents import JobContext

logger = logging.getLogger(__name__)


async def setup_avatar_session(
    ctx: JobContext,
    agent_session,
    provider: Optional[str] = None,
) -> Optional[object]:
    """
    Set up avatar session using LiveKit's built-in avatar support.
    
    This is the recommended approach as it handles all the complexity automatically.
    
    Args:
        ctx: JobContext from the agent entrypoint
        agent_session: The AgentSession instance
        provider: Avatar provider ("tavus" or "beyond-presence")
    
    Returns:
        AvatarSession if successful, None otherwise
    """
    if provider is None:
        provider = os.getenv("AVATAR_PROVIDER", "").lower()
    
    if not provider or provider == "placeholder":
        logger.info("No avatar provider specified, skipping avatar setup")
        return None
    
    try:
        if provider == "tavus":
            return await _setup_tavus_avatar(ctx, agent_session)
        elif provider == "beyond-presence":
            return await _setup_beyond_presence_avatar(ctx, agent_session)
        else:
            logger.warning(f"Unknown avatar provider: {provider}")
            return None
    except ImportError as e:
        logger.warning(f"Avatar plugin not installed: {e}")
        logger.info("Install with: pip install 'livekit-agents[tavus]' or 'livekit-agents[beyond-presence]'")
        return None
    except Exception as e:
        logger.error(f"Failed to setup avatar: {e}")
        import traceback
        traceback.print_exc()
        return None


async def _setup_tavus_avatar(ctx: JobContext, agent_session) -> Optional[object]:
    """
    Set up Tavus avatar using LiveKit's built-in integration.
    
    Requires:
    - TAVUS_API_KEY environment variable
    - TAVUS_REPLICA_ID environment variable
    - TAVUS_PERSONA_ID environment variable (optional)
    
    Note: Avatar session must be started BEFORE agent session starts.
    The avatar will handle audio/video publishing automatically.
    """
    try:
        from livekit.plugins import tavus
        
        tavus_api_key = os.getenv("TAVUS_API_KEY")
        replica_id = os.getenv("TAVUS_REPLICA_ID")
        persona_id = os.getenv("TAVUS_PERSONA_ID")
        
        if not tavus_api_key or not replica_id:
            logger.warning("TAVUS_API_KEY and TAVUS_REPLICA_ID must be set for Tavus avatar")
            return None
        
        logger.info(f"Setting up Tavus avatar - Replica: {replica_id}, Persona: {persona_id or 'default'}")
        
        # Create Tavus avatar session
        # The avatar session will automatically handle audio/video publishing
        avatar = tavus.AvatarSession(
            replica_id=replica_id,
            persona_id=persona_id,
        )
        
        # Start the avatar session BEFORE starting the agent session
        # The avatar will automatically join the room and publish video/audio tracks
        # Audio from the agent will be sent to the avatar for lip-sync
        # Note: start() takes agent_session as first positional argument
        await avatar.start(agent_session, ctx.room)
        
        logger.info("✅ Tavus avatar session started successfully")
        logger.info("   Avatar will handle audio/video publishing - agent audio will be sent to avatar")
        return avatar
        
    except ImportError as e:
        logger.warning(f"Tavus plugin not installed: {e}")
        logger.info("Install with: pip install 'livekit-agents[tavus]'")
        return None
    except Exception as e:
        logger.error(f"Failed to setup Tavus avatar: {e}")
        import traceback
        traceback.print_exc()
        return None


async def _setup_beyond_presence_avatar(ctx: JobContext, agent_session) -> Optional[object]:
    """
    Set up Beyond Presence avatar using LiveKit's built-in integration.
    
    Requires:
    - BEY_API_KEY environment variable (or BEYOND_PRESENCE_API_KEY)
    - BEY_AVATAR_ID environment variable (or BEYOND_PRESENCE_AVATAR_ID)
    
    Note: Avatar session must be started BEFORE agent session starts.
    The avatar will handle audio/video publishing automatically.
    """
    try:
        # Beyond Presence plugin is imported as 'bey' not 'beyond_presence'
        from livekit.plugins import bey
        
        # Check both naming conventions for environment variables
        api_key = os.getenv("BEY_API_KEY") or os.getenv("BEYOND_PRESENCE_API_KEY")
        avatar_id = os.getenv("BEY_AVATAR_ID") or os.getenv("BEYOND_PRESENCE_AVATAR_ID")
        
        if not api_key or not avatar_id:
            logger.warning("BEY_API_KEY (or BEYOND_PRESENCE_API_KEY) and BEY_AVATAR_ID (or BEYOND_PRESENCE_AVATAR_ID) must be set")
            logger.warning(f"   BEY_API_KEY: {'SET' if api_key else 'NOT SET'}")
            logger.warning(f"   BEY_AVATAR_ID: {'SET' if avatar_id else 'NOT SET'}")
            return None
        
        logger.info(f"Setting up Beyond Presence avatar - Avatar ID: {avatar_id}")
        logger.info(f"   API Key: {'SET' if api_key else 'NOT SET'} (length: {len(api_key) if api_key else 0})")
        
        # Create Beyond Presence avatar session
        # Pass api_key explicitly to ensure it's set
        # The avatar session will automatically handle audio/video publishing
        avatar = bey.AvatarSession(
            avatar_id=avatar_id,
            api_key=api_key,  # Pass API key explicitly
        )
        
        # Start the avatar session BEFORE starting the agent session
        # The avatar will automatically join the room and publish video/audio tracks
        # Audio from the agent will be sent to the avatar for lip-sync
        # Note: start() takes agent_session as first positional argument, not session=
        await avatar.start(agent_session, ctx.room)
        
        logger.info("✅ Beyond Presence avatar session started successfully")
        logger.info("   Avatar will handle audio/video publishing - agent audio will be sent to avatar")
        return avatar
        
    except ImportError as e:
        logger.warning(f"Beyond Presence plugin not installed: {e}")
        logger.info("Install with: pip install 'livekit-agents[bey]'")
        return None
    except Exception as e:
        error_str = str(e)
        # Check for concurrency limit error (429)
        if "429" in error_str or "concurrency limit" in error_str.lower():
            logger.warning("⚠️  Beyond Presence concurrency limit reached")
            logger.warning("   This means you have reached the maximum number of concurrent avatar sessions")
            logger.warning("   Solutions:")
            logger.warning("   1. Stop other ongoing Beyond Presence sessions")
            logger.warning("   2. Wait for existing sessions to complete")
            logger.warning("   3. Upgrade your Beyond Presence plan for more concurrent sessions")
            logger.info("   Falling back to placeholder avatar video (if enabled)")
            # Return None so the code can fall back to placeholder video
            return None
        else:
            logger.error(f"Failed to setup Beyond Presence avatar: {e}")
            import traceback
            traceback.print_exc()
            return None
