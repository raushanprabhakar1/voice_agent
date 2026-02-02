"""
LiveKit Voice Agent for Appointment Booking
"""
import asyncio
import json
import os
import logging
from datetime import datetime, timedelta
from typing import Annotated, Literal
from dotenv import load_dotenv

# Enable debug logging with immediate output
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    force=True  # Force reconfiguration
)
logger = logging.getLogger(__name__)

# Print immediately to stdout as well
print("=" * 60)
print("SuperBryn Voice Agent - Starting...")
print("=" * 60)

from livekit import agents, rtc
from livekit.agents import (
    JobContext,
    WorkerOptions,
    cli,
    llm,
    vad,
)
from livekit.agents.voice import Agent, AgentSession
from livekit.agents.worker import JobRequest
from livekit.plugins import deepgram, cartesia

from database import Database
from tools import AppointmentTools

load_dotenv()

# Log startup
logger.info("=" * 60)
logger.info("Starting SuperBryn Voice Agent")
logger.info("=" * 60)

# Check environment variables
logger.info("Checking environment variables...")
required_vars = [
    "LIVEKIT_URL",
    "LIVEKIT_API_KEY", 
    "LIVEKIT_API_SECRET",
    "DEEPGRAM_API_KEY",
    "CARTESIA_API_KEY",
    "SUPABASE_URL",
    "SUPABASE_KEY",
]

for var in required_vars:
    value = os.getenv(var)
    if value:
        logger.info(f"  ✓ {var}: {'*' * min(len(value), 10)}")
    else:
        logger.warning(f"  ✗ {var}: NOT SET")

logger.info(f"LLM_PROVIDER: {os.getenv('LLM_PROVIDER', 'not set')}")
logger.info(f"LLM_MODEL: {os.getenv('LLM_MODEL', 'not set')}")

# Initialize database
try:
    db = Database()
    logger.info("Database initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize database: {e}")
    raise


def _create_llm(tools: list | None = None):
    """Create LLM instance based on provider"""
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    model = os.getenv("LLM_MODEL", "gpt-4o-mini")

    if provider == "openai":
        from livekit.plugins import openai as openai_plugin

        llm_instance = openai_plugin.LLM(model=model)
        # Store tools for later use (tools are passed to chat() method)
        if tools:
            llm_instance._tools = tools
        else:
            llm_instance._tools = []
        return llm_instance

    elif provider == "azure":
        from livekit.plugins import openai as openai_plugin
        from openai import AsyncAzureOpenAI

        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
        azure_api_version = os.getenv(
            "AZURE_OPENAI_API_VERSION", "2024-02-15-preview"
        )
        deployment_name = os.getenv(
            "AZURE_OPENAI_DEPLOYMENT_NAME", model
        )

        if not azure_endpoint or not azure_api_key:
            raise ValueError(
                "AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY must be set for Azure provider"
            )

        # Azure OpenAI endpoint format: https://{resource-name}.openai.azure.com
        azure_endpoint = azure_endpoint.rstrip("/")

        logger.info("Azure OpenAI Configuration:")
        logger.info(f"  Endpoint: {azure_endpoint}")
        logger.info(f"  Deployment Name: {deployment_name}")
        logger.info(f"  API Version: {azure_api_version}")

        # Use AsyncAzureOpenAI which handles Azure URL construction correctly
        # This matches the working Test 2 approach
        client = AsyncAzureOpenAI(
            api_key=azure_api_key,
            api_version=azure_api_version,
            azure_endpoint=azure_endpoint,
        )

        llm_instance = openai_plugin.LLM(
            model=deployment_name,  # Azure deployment name
            client=client,  # Use Azure-configured client
        )
        # Store tools for later use (tools are passed to chat() method)
        if tools:
            llm_instance._tools = tools
        else:
            llm_instance._tools = []
        return llm_instance
    elif provider == "anthropic":
        from livekit.plugins import anthropic as anthropic_plugin
        llm_instance = anthropic_plugin.LLM(model=model)
    elif provider == "together":
        # Together AI uses OpenAI-compatible API
        from livekit.plugins import openai as openai_plugin
        llm_instance = openai_plugin.LLM(
            model=model,
            api_key=os.getenv("TOGETHER_API_KEY"),
            base_url="https://api.together.xyz/v1",
        )
    elif provider == "openrouter":
        from livekit.plugins import openai as openai_plugin
        llm_instance = openai_plugin.LLM(
            model=model,
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1",
        )
    else:
        raise ValueError(f"Unknown LLM provider: {provider}")
    
    # Tools are passed to chat() method, not registered on LLM instance
    # Store tools on the instance for later use
    if tools:
        llm_instance._tools = tools
    else:
        llm_instance._tools = []
    
    return llm_instance


async def _generate_summary(conversation_history: list, tool_calls_made: list) -> dict:
    """Generate conversation summary using LLM"""
    conversation_text = "\n".join([
        f"{msg['role']}: {msg['content']}"
        for msg in conversation_history[-20:]  # Last 20 messages
    ])
    
    summary_prompt = f"""Generate a concise summary of this conversation:

{conversation_text}

Provide a JSON summary with:
- summary: Brief overview of the conversation
- appointments_booked: List of appointments booked (if any)
- appointments_cancelled: List of appointments cancelled (if any)
- appointments_modified: List of appointments modified (if any)
- user_preferences: Any preferences mentioned by the user
- key_points: 3-5 key points from the conversation

Return only valid JSON."""

    llm_instance = _create_llm([])  # No tools needed for summary
    chat_ctx = llm.ChatContext()
    chat_ctx.add_message(role="user", content=summary_prompt)
    
    # llm.chat() returns an LLMStream (async context manager)
    # We need to iterate over it to collect the response
    summary_text = ""
    try:
        async with llm_instance.chat(chat_ctx=chat_ctx) as stream:
            async for chunk in stream:
                if chunk.delta and chunk.delta.content:
                    summary_text += chunk.delta.content
        
        # Extract JSON from response
        if "```json" in summary_text:
            summary_text = summary_text.split("```json")[1].split("```")[0]
        elif "```" in summary_text:
            summary_text = summary_text.split("```")[1].split("```")[0]
        
        summary = json.loads(summary_text.strip())
        summary["timestamp"] = datetime.now().isoformat()
        summary["tool_calls"] = tool_calls_made
        return summary
    except Exception as e:
        logger.warning(f"Failed to generate summary: {e}")
        # Fallback summary
        return {
            "summary": "Conversation completed",
            "appointments_booked": [],
            "appointments_cancelled": [],
            "appointments_modified": [],
            "user_preferences": [],
            "key_points": [],
            "timestamp": datetime.now().isoformat(),
            "tool_calls": tool_calls_made,
            "error": str(e),
        }


async def job_request_handler(req: JobRequest) -> None:
    """Called when LiveKit wants to assign a job to this agent"""
    print("\n" + "=" * 60)
    print("📥 JOB REQUEST RECEIVED!")
    print("=" * 60)
    logger.info("=" * 60)
    logger.info("📥 JOB REQUEST RECEIVED!")
    logger.info(f"   Job ID: {req.id}")
    logger.info(f"   Room: {req.room.name}")
    logger.info(f"   Room SID: {req.room.sid}")
    
    # Get participant info if available
    publisher = req.publisher
    if publisher:
        logger.info(f"   Publisher: {publisher.identity}")
        logger.info(f"   Publisher Name: {publisher.name}")
        logger.info(f"   Publisher Metadata: {publisher.metadata}")
    else:
        logger.info("   Publisher: None (room-level job)")
    
    logger.info(f"   Agent Name: {req.agent_name}")
    logger.info("=" * 60)
    print(f"   Room: {req.room.name}")
    if publisher:
        print(f"   Participant: {publisher.identity}")
    print("=" * 60 + "\n")
    
    # Accept the job - this is required!
    try:
        await req.accept()
        logger.info("✅ Job accepted - entrypoint will be called")
        print("✅ Job accepted - entrypoint will be called\n")
    except Exception as e:
        logger.error(f"❌ Error accepting job: {e}")
        print(f"❌ Error accepting job: {e}\n")
        import traceback
        traceback.print_exc()
        raise


async def entrypoint(ctx: JobContext):
    """Entry point for the agent"""
    logger.info("=" * 60)
    logger.info("🚀 AGENT ENTRYPOINT CALLED!")
    logger.info(f"   Room: {ctx.room.name}")
    logger.info(f"   Job ID: {getattr(ctx, 'job_id', 'unknown')}")
    logger.info("=" * 60)
    
    try:
        logger.info("Connecting to room...")
        await ctx.connect()
        logger.info(f"✅ Connected to room: {ctx.room.name}")
        # Room.sid might be a coroutine - try to get it safely
        try:
            room_sid = ctx.room.sid
            if asyncio.iscoroutine(room_sid):
                room_sid = await room_sid
            logger.info(f"   Room SID: {room_sid}")
        except Exception as e:
            logger.info(f"   Room SID: (could not get: {e})")
        logger.info(f"   Local participant: {ctx.room.local_participant.identity}")
    except Exception as e:
        logger.error(f"❌ Failed to connect to room: {e}")
        import traceback
        traceback.print_exc()
        raise
    
    # Subscribe to all audio tracks from remote participants
    # Note: Event handlers must be synchronous, use asyncio.create_task for async operations
    def on_track_published(publication: rtc.RemoteTrackPublication, participant: rtc.RemoteParticipant):
        track_kind_name = "AUDIO" if publication.kind == rtc.TrackKind.KIND_AUDIO else "VIDEO" if publication.kind == rtc.TrackKind.KIND_VIDEO else "UNKNOWN"
        logger.info(f"Track published: {track_kind_name} (kind={publication.kind}) from {participant.identity}")
        
        if participant.identity == "bey-avatar-agent":
            if publication.kind == rtc.TrackKind.KIND_VIDEO:
                logger.info("🎥 ✅ Beyond Presence VIDEO track published! This is what we need for the avatar.")
            elif publication.kind == rtc.TrackKind.KIND_AUDIO:
                logger.info("🔊 Beyond Presence audio track published (expected)")
        
        if publication.kind == rtc.TrackKind.KIND_AUDIO:
            logger.info("Audio track published - subscribing...")
            async def subscribe():
                try:
                    await publication.set_subscribed(True)
                    logger.info("Audio track subscription set to True")
                except Exception as e:
                    logger.error(f"Error subscribing to audio track: {e}")
            asyncio.create_task(subscribe())
        elif publication.kind == rtc.TrackKind.KIND_VIDEO:
            logger.info(f"🎥 Video track published from {participant.identity} - frontend should subscribe to this")
            if participant.identity == "bey-avatar-agent":
                logger.info("   ✅ This is the Beyond Presence avatar video track!")
    
    def on_track_subscribed(track: rtc.Track, publication: rtc.TrackPublication, participant: rtc.RemoteParticipant):
        track_kind_name = "AUDIO" if track.kind == rtc.TrackKind.KIND_AUDIO else "VIDEO" if track.kind == rtc.TrackKind.KIND_VIDEO else "UNKNOWN"
        logger.info(f"Track subscribed: {track_kind_name} (kind={track.kind}) from {participant.identity}")
        
        if participant.identity == "bey-avatar-agent":
            if track.kind == rtc.TrackKind.KIND_VIDEO:
                logger.info("🎥 ✅ Beyond Presence VIDEO track subscribed! Frontend should display avatar now.")
            elif track.kind == rtc.TrackKind.KIND_AUDIO:
                logger.info("🔊 Beyond Presence audio track subscribed (expected)")
        
        if track.kind == rtc.TrackKind.KIND_AUDIO:
            logger.info("Audio track subscribed - agent should receive audio now")
        elif track.kind == rtc.TrackKind.KIND_VIDEO:
            logger.info(f"🎥 Video track subscribed from {participant.identity} - frontend should display this")
    
    def on_participant_connected(participant: rtc.RemoteParticipant):
        logger.info(f"Participant connected: {participant.identity}")
        # Log participant count
        remote_count = len(list(ctx.room.remote_participants.values()))
        logger.info(f"   Total remote participants: {remote_count}")
        if participant.identity == "bey-avatar-agent":
            logger.info("   ✅ Beyond Presence avatar participant joined (this is expected)")
        # Subscribe to their audio tracks
        async def subscribe_to_tracks():
            for publication in participant.track_publications.values():
                if publication.kind == rtc.TrackKind.KIND_AUDIO:
                    logger.info(f"Subscribing to audio from {participant.identity}")
                    try:
                        await publication.set_subscribed(True)
                    except Exception as e:
                        logger.error(f"Error subscribing to track: {e}")
        asyncio.create_task(subscribe_to_tracks())
    
    ctx.room.on("track_published", on_track_published)
    ctx.room.on("track_subscribed", on_track_subscribed)
    ctx.room.on("participant_connected", on_participant_connected)
    
    # Subscribe to existing tracks
    for participant in ctx.room.remote_participants.values():
        logger.info(f"Checking participant: {participant.identity}")
        for publication in participant.track_publications.values():
            if publication.kind == rtc.TrackKind.KIND_AUDIO:
                # Check subscription status - subscribed() is a method
                is_subscribed = publication.subscribed() if hasattr(publication, 'subscribed') and callable(publication.subscribed) else False
                logger.info(f"Audio track found from {participant.identity}, subscribed={is_subscribed}")
                if not is_subscribed:
                    try:
                        # set_subscribed is synchronous, not awaitable
                        publication.set_subscribed(True)
                        logger.info(f"Subscribed to audio track from {participant.identity}")
                    except Exception as e:
                        logger.warning(f"Could not subscribe to track: {e}")
    
    # Create tools instance
    tools_instance = AppointmentTools(db)
    tool_definitions = tools_instance.get_tool_definitions()
    logger.info(f"Created {len(tool_definitions)} tools")
    
    # Track conversation state
    conversation_history = []
    tool_calls_made = []
    user_phone = [None]  # Use list to allow modification in nested function
    
    # Create LLM with tools
    # Note: Tools are passed to Agent, and AgentSession will handle tool execution automatically
    llm_instance = _create_llm(tool_definitions)
    
    # Verify Deepgram API key is set
    deepgram_key = os.environ.get("DEEPGRAM_API_KEY")
    if not deepgram_key:
        logger.error("DEEPGRAM_API_KEY not set! STT will not work.")
    else:
        logger.info(f"Deepgram API key found (length: {len(deepgram_key)})")
    
    # Verify Cartesia API key is set
    cartesia_key = os.environ.get("CARTESIA_API_KEY")
    if not cartesia_key:
        logger.error("CARTESIA_API_KEY not set! TTS will not work.")
    else:
        logger.info(f"Cartesia API key found (length: {len(cartesia_key)})")
    
    # Create voice assistant
    logger.info("Creating VoiceAssistant with STT and TTS...")
    try:
        stt_instance = deepgram.STT()
        logger.info("Deepgram STT instance created")
    except Exception as e:
        logger.error(f"Failed to create Deepgram STT: {e}")
        raise
    
    try:
        tts_instance = cartesia.TTS()
        logger.info("Cartesia TTS instance created")
    except Exception as e:
        logger.error(f"Failed to create Cartesia TTS: {e}")
        raise
    
    # Create ChatContext with system message
    system_chat_ctx = llm.ChatContext()
    system_chat_ctx.add_message(
        role="system",
        content="""You are a friendly and professional appointment booking assistant. 
Your role is to help users book, retrieve, modify, and cancel appointments.

Guidelines:
- Be conversational and natural
- Always confirm appointment details before booking
- If a user wants to book, first identify them by asking for their phone number
- When booking, confirm the date, time, and any other details
- Prevent double-booking by checking availability
- Be helpful and empathetic
- Keep responses concise (under 30 seconds of speech)
- When ending a conversation, summarize what was discussed""",
    )
    
    assistant = Agent(
        instructions="""You are a friendly and professional appointment booking assistant. 
Your role is to help users book, retrieve, modify, and cancel appointments.

Guidelines:
- Be conversational and natural
- Always confirm appointment details before booking
- If a user wants to book, first identify them by asking for their phone number
- When user wants to book an appointment:
  1. First call fetch_slots to get available slots (this returns ONLY available slots)
  2. Present the available slots to the user
  3. Book the first available slot (or the slot the user prefers)
- The fetch_slots tool already filters out booked slots, so you can book any slot it returns
- Always confirm the date, time, and any other details before booking
- Be helpful and empathetic
- Keep responses concise (under 30 seconds of speech)
- When ending a conversation, summarize what was discussed

Available tools:
- identify_user: Get user's phone number to identify them
- fetch_slots: Get available appointment slots (returns ONLY unbooked slots)
- book_appointment: Book an appointment (use slots from fetch_slots)
- retrieve_appointments: Get user's past appointments
- cancel_appointment: Cancel an appointment
- modify_appointment: Change appointment details
- end_conversation: End the call and generate summary""",
        vad=None,  # VAD will be auto-detected or use STT-based turn detection
        stt=stt_instance,
        llm=llm_instance,
        tts=tts_instance,
        tools=tool_definitions,
        chat_ctx=system_chat_ctx,
    )
    
    # Start the assistant session
    logger.info("Starting assistant session with room...")
    
    # Note: Avatar video track will be published AFTER session starts
    # This ensures the room is fully connected before publishing video
    
    # Import event types
    from livekit.agents.voice.events import (
        UserInputTranscribedEvent,
        ConversationItemAddedEvent,
        FunctionToolsExecutedEvent,
        AgentEvent,
    )
    
    # Create AgentSession - don't pass tools here since Agent already has them
    # AgentSession will use tools from the Agent when we call start(agent=assistant)
    session = AgentSession(
        stt=stt_instance,
        llm=llm_instance,
        tts=tts_instance,
        # Don't pass tools here - they're already in the Agent
        turn_detection="stt",  # Use STT-based turn detection
    )
    
    # Set up event handlers for conversation tracking BEFORE starting
    def on_event(ev: AgentEvent):
        if isinstance(ev, UserInputTranscribedEvent):
            if ev.is_final:
                logger.info(f"🎤 USER SPEECH RECEIVED: {ev.transcript}")
                conversation_history.append({
                    "role": "user",
                    "content": ev.transcript,
                    "timestamp": datetime.now().isoformat(),
                })
            else:
                logger.info(f"🎤 USER SPEECH (partial): {ev.transcript}")
        elif isinstance(ev, ConversationItemAddedEvent):
            if hasattr(ev.item, 'role') and hasattr(ev.item, 'content'):
                role = ev.item.role
                content = ev.item.content
                if isinstance(content, list):
                    # Extract text from content list
                    text = " ".join([str(c) for c in content if isinstance(c, str)])
                else:
                    text = str(content)
                
                if role == "assistant":
                    logger.info(f"🤖 ASSISTANT SPEECH: {text}")
                    conversation_history.append({
                        "role": "assistant",
                        "content": text,
                        "timestamp": datetime.now().isoformat(),
                    })
        elif isinstance(ev, FunctionToolsExecutedEvent):
            # Track tool calls
            for function_call, function_output in ev.zipped():
                logger.info(f"🔧 TOOL CALL: {function_call.name}")
                tool_calls_made.append({
                    "name": function_call.name,
                    "args": function_call.arguments,
                    "result": function_output.output if function_output else None,
                    "timestamp": datetime.now().isoformat(),
                })
                
                # Generate unique ID for this tool call
                import uuid
                tool_call_id = str(uuid.uuid4())
                
                # Send tool call info to frontend
                try:
                    # Parse arguments if it's a string
                    args_data = function_call.arguments
                    if isinstance(args_data, str):
                        try:
                            args_data = json.loads(args_data)
                        except:
                            pass  # Keep as string if not JSON
                    
                    tool_call_data = {
                        "type": "tool_call",
                        "id": tool_call_id,
                        "name": function_call.name,
                        "args": args_data,
                    }
                    logger.info(f"📤 Sending tool_call to frontend: {function_call.name} (ID: {tool_call_id})")
                    logger.info(f"   Room participants: {len(ctx.room.remote_participants)}")
                    for pid, participant in ctx.room.remote_participants.items():
                        logger.info(f"   - Remote participant: {participant.identity}")
                    
                    # Send data - publish_data is async, but on_event is sync, so use create_task
                    try:
                        data_bytes = json.dumps(tool_call_data).encode('utf-8')
                        logger.info(f"   📦 Data bytes: {len(data_bytes)} bytes")
                        logger.info(f"   📦 Data content: {tool_call_data}")
                        
                        # Send to each remote participant explicitly
                        remote_participants_list = list(ctx.room.remote_participants.values())
                        logger.info(f"   📤 Sending to {len(remote_participants_list)} remote participant(s)")
                        
                        if len(remote_participants_list) == 0:
                            logger.warning("   ⚠️  No remote participants to send data to!")
                        else:
                            # Send data once (with topic)
                            # IMPORTANT: publish_data is async, but on_event is sync, so use create_task
                            try:
                                asyncio.create_task(
                                    ctx.room.local_participant.publish_data(
                                        data_bytes,
                                        topic="tool_calls",
                                        reliable=True,
                                    )
                                )
                                logger.info(f"   ✅ Tool call sent with topic 'tool_calls' (async task created)")
                            except Exception as e_topic:
                                logger.error(f"   ❌ Failed to send with topic: {e_topic}")
                                import traceback
                                traceback.print_exc()
                                # Only try fallback if topic send fails
                                try:
                                    asyncio.create_task(
                                        ctx.room.local_participant.publish_data(
                                            data_bytes,
                                            reliable=True,
                                        )
                                    )
                                    logger.info(f"   ✅ Tool call sent without topic (fallback)")
                                except Exception as e2:
                                    logger.error(f"   ❌ Fallback send also failed: {e2}")
                                    import traceback
                                    traceback.print_exc()
                    except Exception as e:
                        logger.error(f"   ❌ Error sending tool call: {e}")
                        import traceback
                        traceback.print_exc()
                except Exception as e:
                    logger.error(f"❌ Error sending tool call to frontend: {e}")
                    import traceback
                    traceback.print_exc()
                
                # Send tool result to frontend
                if function_output:
                    try:
                        # FunctionCallOutput has 'output' attribute, not 'content'
                        result_output = function_output.output if hasattr(function_output, 'output') else str(function_output)
                        # Try to parse as JSON if it's a string
                        try:
                            result_output = json.loads(result_output) if isinstance(result_output, str) else result_output
                        except (json.JSONDecodeError, TypeError):
                            pass  # Keep as string if not JSON
                        
                        tool_result_data = {
                            "type": "tool_result",
                            "id": tool_call_id,  # Include the same ID for matching
                            "name": function_call.name,
                            "result": result_output,
                        }
                        logger.info(f"📤 Sending tool_result to frontend: {function_call.name} (ID: {tool_call_id})")
                        logger.info(f"   Room participants: {len(ctx.room.remote_participants)}")
                        for pid, participant in ctx.room.remote_participants.items():
                            logger.info(f"   - Remote participant: {participant.identity}")
                        
                        # Send data - publish_data is synchronous, not async
                        try:
                            data_bytes_result = json.dumps(tool_result_data).encode('utf-8')
                            logger.info(f"   📦 Result bytes: {len(data_bytes_result)} bytes")
                            logger.info(f"   📦 Result content: {tool_result_data}")
                            
                            remote_participants_list = list(ctx.room.remote_participants.values())
                            logger.info(f"   📤 Sending result to {len(remote_participants_list)} remote participant(s)")
                            
                            if len(remote_participants_list) == 0:
                                logger.warning("   ⚠️  No remote participants to send result to!")
                            else:
                                # Send result once (with topic)
                                # IMPORTANT: publish_data is async, but on_event is sync, so use create_task
                                try:
                                    asyncio.create_task(
                                        ctx.room.local_participant.publish_data(
                                            data_bytes_result,
                                            topic="tool_results",
                                            reliable=True,
                                        )
                                    )
                                    logger.info(f"   ✅ Tool result sent with topic 'tool_results' (async task created)")
                                except Exception as e_topic:
                                    logger.error(f"   ❌ Failed to send result with topic: {e_topic}")
                                    import traceback
                                    traceback.print_exc()
                                    # Only try fallback if topic send fails
                                    try:
                                        asyncio.create_task(
                                            ctx.room.local_participant.publish_data(
                                                data_bytes_result,
                                                reliable=True,
                                            )
                                        )
                                        logger.info(f"   ✅ Tool result sent without topic (fallback)")
                                    except Exception as e2:
                                        logger.error(f"   ❌ Fallback send also failed: {e2}")
                                        import traceback
                                        traceback.print_exc()
                        except Exception as e:
                            logger.error(f"   ❌ Error sending tool result: {e}")
                            import traceback
                            traceback.print_exc()
                    except Exception as e:
                        logger.error(f"❌ Error sending tool result to frontend: {e}")
                        import traceback
                        traceback.print_exc()
                
                # Update user_phone if identify_user was called
                if function_call.name == "identify_user":
                    args = json.loads(function_call.arguments) if isinstance(
                        function_call.arguments, str
                    ) else function_call.arguments
                    if "phone" in args:
                        user_phone[0] = args["phone"]
                        tools_instance.user_phone = args["phone"]
    
    # Register event handlers
    session.on("user_input_transcribed", on_event)
    session.on("conversation_item_added", on_event)
    session.on("function_tools_executed", on_event)
    logger.info("✅ Registered event handlers for conversation tracking")
    
    # Set up avatar - two modes:
    # 1. Separate participant mode (AVATAR_MODE=separate or not set): Avatar joins as separate participant (3 participants)
    # 2. Direct mode (AVATAR_MODE=direct): Agent publishes video directly (2 participants)
    avatar_session = None
    avatar_mode = os.getenv("AVATAR_MODE", "separate").lower()
    avatar_provider = os.getenv("AVATAR_PROVIDER", "").lower()
    
    logger.info(f"🔍 Avatar provider: '{avatar_provider}', mode: '{avatar_mode}'")
    
    # Direct mode: Agent publishes video directly (2 participants)
    if avatar_mode == "direct":
        logger.info("📹 Using direct video mode - agent will publish video directly (2 participants)")
        # Don't create separate avatar session, agent will publish video directly
        avatar_session = None
    # Separate participant mode: Avatar joins as separate participant (3 participants)
    elif avatar_provider in ["tavus", "beyond-presence"]:
        try:
            from avatar_integration import setup_avatar_session
            logger.info(f"Setting up {avatar_provider} avatar as separate participant (3 participants)...")
            avatar_session = await setup_avatar_session(ctx, session, provider=avatar_provider)
            if avatar_session:
                logger.info("✅ Avatar session created - avatar will join as separate participant")
                logger.info(f"   Avatar session type: {type(avatar_session).__name__}")
                logger.info("   Note: This creates 3 participants (user + agent + avatar)")
                # When using avatar, the avatar handles audio/video publishing
                # The agent session will send audio to the avatar for lip-sync
            else:
                logger.warning(f"❌ Avatar session creation failed - continuing without avatar")
                logger.warning(f"   Check backend logs above for specific error messages")
                logger.warning(f"   Verify: AVATAR_PROVIDER={avatar_provider}, API keys set, plugin installed")
        except ImportError as e:
            logger.warning(f"Avatar integration module not available: {e}")
            logger.info("Using direct audio output (no avatar)")
        except Exception as e:
            logger.error(f"❌ Avatar setup failed with exception: {e}")
            import traceback
            traceback.print_exc()
    else:
        logger.info(f"Avatar provider '{avatar_provider}' not in ['tavus', 'beyond-presence'] - using direct video mode")
    
    # Start the session with the Agent and room
    # session.start() is an async function, not a context manager
    # IMPORTANT: If avatar is active, it will automatically receive audio from the agent
    # and publish synchronized video/audio tracks to the room
    logger.info("Starting agent session...")
    
    await session.start(
        agent=assistant,
        room=ctx.room,
        # Note: If avatar_session is active, the avatar will handle audio/video publishing
        # The agent's audio output will be sent to the avatar for lip-sync
    )
    logger.info("Voice assistant started - waiting for audio input...")
    
    # Publish avatar video track directly from agent (2 participants mode)
    # This happens when:
    # 1. AVATAR_MODE=direct (agent publishes video directly)
    # 2. OR avatar_session is None (fallback or placeholder)
    # This gives you 2 participants: user + agent (agent publishes video)
    if not avatar_session:
        try:
            enable_avatar_video = os.getenv("ENABLE_AVATAR_VIDEO", "false").lower() == "true"
            avatar_provider = os.getenv("AVATAR_PROVIDER", "placeholder").lower()
            
            # If user wanted Beyond Presence/Tavus but it failed, enable placeholder as fallback
            if avatar_provider in ["beyond-presence", "tavus"]:
                logger.info("⚠️  Real avatar unavailable - enabling placeholder video as fallback")
                enable_avatar_video = True
            
            if enable_avatar_video:
                from avatar_video import publish_avatar_video
                # Use the configured provider (beyond-presence, tavus, or placeholder)
                # In direct mode, agent will stream video from the provider and publish it
                logger.info(f"Publishing avatar video track directly from agent (provider: {avatar_provider})...")
                logger.info("   Mode: Direct (2 participants: user + agent)")
                video_track = await publish_avatar_video(ctx, provider=avatar_provider)
                if video_track:
                    logger.info("✅ Avatar video track published successfully by agent")
                    logger.info("   Participants: 2 (user + agent with video)")
                    if avatar_provider == "placeholder":
                        logger.info("   Note: Using placeholder video. For real avatar, configure Beyond Presence/Tavus API.")
                else:
                    logger.warning("Avatar video track not published - check logs above for errors")
            else:
                logger.info("Placeholder avatar video not enabled (set ENABLE_AVATAR_VIDEO=true to enable)")
        except ImportError:
            logger.info("avatar_video module not available - skipping placeholder video track publishing")
        except Exception as e:
            logger.warning(f"Failed to publish placeholder avatar video track: {e}")
            import traceback
            traceback.print_exc()
            # Don't fail the entire agent if video publishing fails
    else:
        logger.info("Using real avatar (Tavus/Beyond Presence) - video publishing handled automatically")
    
    # Add periodic logging to check if assistant is still running
    async def periodic_check():
        while True:
            await asyncio.sleep(5)
            remote_participants = list(ctx.room.remote_participants.values())
            logger.info(f"Periodic check - Remote participants: {len(remote_participants)}")
            for participant in remote_participants:
                audio_count = 0
                video_count = 0
                for pub in participant.track_publications.values():
                    if pub.kind == rtc.TrackKind.KIND_AUDIO:
                        audio_count += 1
                        is_subscribed = pub.subscribed() if hasattr(pub, 'subscribed') and callable(pub.subscribed) else False
                        is_muted = pub.muted() if hasattr(pub, 'muted') and callable(pub.muted) else False
                        logger.info(f"  Audio track #{audio_count} from {participant.identity}: subscribed={is_subscribed}, muted={is_muted}")
                    elif pub.kind == rtc.TrackKind.KIND_VIDEO:
                        video_count += 1
                        is_subscribed = pub.subscribed() if hasattr(pub, 'subscribed') and callable(pub.subscribed) else False
                        is_muted = pub.muted() if hasattr(pub, 'muted') and callable(pub.muted) else False
                        logger.info(f"  🎥 Video track #{video_count} from {participant.identity}: subscribed={is_subscribed}, muted={is_muted}")
                        if participant.identity == "bey-avatar-agent":
                            logger.info(f"     ✅ This is the Beyond Presence avatar video track!")
                
                if participant.identity == "bey-avatar-agent":
                    if video_count == 0:
                        logger.warning(f"  ⚠️  bey-avatar-agent has NO video tracks yet (has {audio_count} audio tracks)")
                        logger.warning(f"     Beyond Presence may still be initializing video stream...")
                    else:
                        logger.info(f"  ✅ bey-avatar-agent has {video_count} video track(s) - avatar should be visible")
    
    # Start periodic check in background
    asyncio.create_task(periodic_check())
    
    # Wait for room to disconnect
    try:
        # Wait until room disconnects
        disconnect_event = asyncio.Event()
        
        def on_disconnect():
            print("Room disconnected")
            disconnect_event.set()
        
        # Listen for room disconnect
        if hasattr(ctx.room, 'on'):
            ctx.room.on("disconnected", on_disconnect)
        
        # Also wait for assistant to finish
        # Keep running until disconnect (max 1 hour)
        try:
            await asyncio.wait_for(disconnect_event.wait(), timeout=3600)
        except asyncio.TimeoutError:
            print("Session timeout reached (1 hour)")
    except Exception as e:
        print(f"Error waiting for disconnect: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Generate summary when done
        if len(conversation_history) > 0 or len(tool_calls_made) > 0:
            summary = await _generate_summary(conversation_history, tool_calls_made)
            
            # Save summary to database
            if user_phone[0]:
                await db.save_conversation_summary(
                    user_phone=user_phone[0],
                    summary=summary,
                    tool_calls=tool_calls_made,
                )
            
            # Send summary to frontend
            try:
                await ctx.room.local_participant.publish_data(
                    json.dumps({
                        "type": "conversation_summary",
                        "summary": summary,
                    }).encode(),
                    topic="summary",
                )
            except Exception as e:
                print(f"Error sending summary: {e}")
        
        # Clean up session
        await session.aclose()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("REGISTERING AGENT ENTRYPOINT")
    print("=" * 60 + "\n")
    
    logger.info("=" * 60)
    logger.info("Registering agent entrypoint...")
    logger.info("=" * 60)
    
    try:
        print("Starting LiveKit agent worker...")
        print("Agent will listen for new connections on LiveKit server")
        print(f"LiveKit URL: {os.getenv('LIVEKIT_URL', 'NOT SET')}")
        print("\nWaiting for user connections...")
        print("(The entrypoint will be called when a user connects)\n")
        
        logger.info("Starting LiveKit agent worker...")
        logger.info("Agent will listen for new connections on LiveKit server")
        logger.info(f"LiveKit URL: {os.getenv('LIVEKIT_URL', 'NOT SET')}")
        logger.info("Waiting for user connections...")
        logger.info("(The entrypoint will be called when a user connects)")
        
        # Configure worker options
        # For explicit dispatch on LiveKit Cloud, we need to set an agent name
        agent_name = "voice-agent"  # Set name for explicit dispatch
        worker_opts = WorkerOptions(
            entrypoint_fnc=entrypoint,
            request_fnc=job_request_handler,
            agent_name=agent_name,  # Set name for explicit dispatch
        )
        
        logger.info("Worker configuration:")
        logger.info(f"  - Agent name: '{agent_name}' (explicit dispatch)")
        logger.info("  - Job type: ROOM")
        logger.info("  - Agent will be dispatched via AgentDispatch API")
        
        logger.info("Worker options configured:")
        logger.info(f"  - Entrypoint: {entrypoint.__name__}")
        logger.info("  - Job request handler: enabled (will log when jobs are received)")
        logger.info("  - Agent will accept jobs and join rooms when participants connect")
        
        cli.run_app(worker_opts)
    except KeyboardInterrupt:
        print("\nAgent stopped by user")
        logger.info("Agent stopped by user")
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        logger.error(f"Fatal error starting agent: {e}")
        import traceback
        traceback.print_exc()
        raise
