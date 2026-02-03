import { useState, useRef } from 'react'
import { Room, RoomEvent, RemoteParticipant, DataPacket_Kind } from 'livekit-client'
import VoiceAgent from './components/VoiceAgent'
import ToolCallDisplay from './components/ToolCallDisplay'
import ConversationSummary from './components/ConversationSummary'
import './App.css'

interface ToolCall {
  id: string
  name: string
  args: any
  result?: any
  timestamp: string
}

interface ConversationSummaryData {
  summary: string
  appointments_booked: any[]
  appointments_cancelled: any[]
  appointments_modified: any[]
  user_preferences: string[]
  key_points: string[]
  timestamp: string
  tool_calls: ToolCall[]
}

function App() {
  const [room, setRoom] = useState<Room | null>(null)
  const [isConnected, setIsConnected] = useState(false)
  const [toolCalls, setToolCalls] = useState<ToolCall[]>([])
  const [summary, setSummary] = useState<ConversationSummaryData | null>(null)
  const [error, setError] = useState<string | null>(null)
  const roomRef = useRef<Room | null>(null)


  const connectToRoom = async () => {
    try {
      setError(null)
      
      // Request microphone permission first
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
        // Stop the stream immediately - we just needed permission
        stream.getTracks().forEach(track => track.stop())
      } catch (permErr: any) {
        if (permErr.name === 'NotAllowedError' || permErr.name === 'PermissionDeniedError') {
          setError('Microphone permission denied. Please allow microphone access in your browser settings and try again.')
          return
        } else if (permErr.name === 'NotFoundError') {
          setError('No microphone found. Please connect a microphone and try again.')
          return
        } else {
          setError(`Microphone error: ${permErr.message}. Please check your browser settings.`)
          return
        }
      }
      
      // Get access token from backend
      const LIVEKIT_URL = (import.meta.env?.VITE_LIVEKIT_URL as string) || 'wss://your-livekit-server.com'
      
      console.log('🔑 Requesting access token from /api/token...')
      console.log('   LiveKit URL:', LIVEKIT_URL)
      
      let response: Response
      try {
        response = await fetch('/api/token', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            room: 'voice-agent-room',
            participant: `user-${Date.now()}`,
          }),
        })
      } catch (fetchError: any) {
        console.error('❌ Fetch error:', fetchError)
        throw new Error(`Failed to reach token API: ${fetchError.message}. Make sure the token API is deployed and accessible.`)
      }
      
      console.log('📡 Token API response status:', response.status, response.statusText)
      
      if (!response.ok) {
        let errorMessage = 'Failed to get access token'
        let errorDetails = ''
        
        // Try to get error details from response
        try {
          const text = await response.text()
          console.error('❌ Token API error response:', text)
          
          if (text) {
            try {
              const errorData = JSON.parse(text)
              errorDetails = errorData.error || errorData.message || text
            } catch {
              errorDetails = text
            }
          } else {
            errorDetails = response.statusText || 'Unknown error'
          }
        } catch (parseError) {
          console.error('❌ Failed to read error response:', parseError)
          errorDetails = response.statusText || 'Unknown error'
        }
        
        // Build error message
        if (errorDetails) {
          errorMessage = errorDetails
        }
        
        // Provide helpful error messages based on status code
        if (response.status === 500) {
          if (!errorMessage.includes('LIVEKIT') && !errorMessage.includes('environment variables')) {
            errorMessage += '. Check that LIVEKIT_API_KEY, LIVEKIT_API_SECRET, and LIVEKIT_URL are set in your Vercel deployment settings (Settings → Environment Variables).'
          }
        } else if (response.status === 404) {
          errorMessage += '. The token API endpoint was not found. Make sure frontend/api/token.ts exists and is deployed correctly (Vercel) or netlify/functions/token.js (Netlify).'
        } else if (response.status === 405) {
          errorMessage += '. The token API only accepts POST requests.'
        }
        
        throw new Error(errorMessage)
      }
      
      const responseData = await response.json().catch(async (parseError) => {
        const text = await response.text().catch(() => '')
        console.error('❌ Failed to parse token API response:', parseError, 'Response:', text)
        throw new Error('Token API returned invalid JSON response')
      })
      
      const { token, url } = responseData
      
      if (!token) {
        console.error('❌ Token API response missing token:', responseData)
        throw new Error('Token API response missing token field')
      }
      
      const finalUrl = url || LIVEKIT_URL
      console.log('✅ Access token received successfully')
      console.log('   LiveKit URL:', finalUrl)
      
      const newRoom = new Room()
      roomRef.current = newRoom // Store in ref for access in handlers
      
      // Listen for data messages - listen to ALL data, not just specific topics
      // IMPORTANT: This must be set up BEFORE connecting to the room
      console.log('🔧 Setting up DataReceived event listener...')
      
      // Create a persistent handler that won't be garbage collected
      // IMPORTANT: Store handler reference to prevent garbage collection
      const dataReceivedHandler = (payload: Uint8Array, _participant: RemoteParticipant | undefined, kind: DataPacket_Kind | undefined, _topic: string | undefined) => {
        if (!payload || payload.length === 0) {
          return
        }
        
        const payloadStr = new TextDecoder().decode(payload)
        
        // Accept both RELIABLE and LOSSY data packets
        if (kind === DataPacket_Kind.RELIABLE || kind === DataPacket_Kind.LOSSY) {
          try {
            const data = JSON.parse(payloadStr)
            
            if (data.type === 'tool_call') {
              console.log('🔧 Tool call received:', data.name, data.id)
              
              // Parse args if it's a string
              let parsedArgs = data.args
              if (typeof data.args === 'string') {
                try {
                  parsedArgs = JSON.parse(data.args)
                } catch {
                  parsedArgs = data.args
                }
              }
              
              // Generate unique ID for this tool call
              const toolCallId = data.id || `${data.name}-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
              
              setToolCalls(prev => {
                // Check if a tool call with this ID already exists (prevent duplicates)
                const existingIndex = prev.findIndex(tc => tc.id === toolCallId)
                if (existingIndex !== -1) {
                  console.log(`⚠️ Duplicate tool call with ID ${toolCallId} ignored`)
                  return prev // Don't add duplicate
                }
                
                const newCall: ToolCall = {
                  id: toolCallId,
                  name: data.name,
                  args: parsedArgs,
                  timestamp: new Date().toISOString(),
                }
                console.log(`✅ Tool call added: ${data.name} (Total: ${prev.length + 1})`)
                return [...prev, newCall]
              })
            } else if (data.type === 'tool_result') {
              console.log('✅ Tool result received:', data.name)
              
              // Check if this is end_conversation - disconnect the call
              if (data.name === 'end_conversation') {
                console.log('👋 End conversation tool called - disconnecting...')
                // Small delay to ensure summary is received first
                setTimeout(() => {
                  const currentRoom = roomRef.current
                  if (currentRoom) {
                    currentRoom.disconnect()
                    setRoom(null)
                    setIsConnected(false)
                    setToolCalls([])
                    setSummary(null)
                    roomRef.current = null
                    console.log('✅ Call disconnected after end_conversation')
                  }
                }, 1000) // 1 second delay to allow summary to arrive
              }
              
              setToolCalls(prev => {
                const updated = [...prev]
                
                // Match by ID first (most reliable) - only update ONE entry
                if (data.id) {
                  const index = updated.findIndex(tc => tc.id === data.id && !tc.result)
                  if (index !== -1) {
                    updated[index].result = data.result
                    console.log(`✅ Tool result updated: ${data.name}`)
                    return [...updated] // Return immediately after first match
                  }
                }
                
                // Fallback: match by name (find the FIRST pending call with this name)
                const pendingIndex = updated.findIndex(tc => tc.name === data.name && !tc.result)
                if (pendingIndex !== -1) {
                  updated[pendingIndex].result = data.result
                  console.log(`✅ Tool result updated by name: ${data.name}`)
                  return [...updated] // Return immediately after first match
                }
                
                // If still not found, don't create a new entry - just log a warning
                console.warn(`⚠️ No matching pending tool call found for result: ${data.name}`)
                return updated // Don't modify if no match found
              })
            } else if (data.type === 'conversation_summary') {
              console.log('📝 Conversation summary received')
              setSummary(data.summary)
            } else {
              console.log('⚠️ Unknown data type:', data.type, data)
            }
          } catch (e: any) {
            console.error('❌❌❌ Error parsing data message:', e)
            console.error('   Error:', e.message)
            console.error('   Payload string:', payloadStr)
            console.error('   Payload length:', payloadStr.length)
          }
        } else {
          console.log('⚠️ Data packet kind not RELIABLE or LOSSY:', kind)
        }
      }
      
      // Register DataReceived listener BEFORE connecting
      newRoom.on(RoomEvent.DataReceived, dataReceivedHandler)
      console.log('✅ DataReceived event listener registered')
      
      // Also verify the listener is actually registered
      const listenerCount = newRoom.listenerCount(RoomEvent.DataReceived)
      console.log('🔍 Verifying event listener:', {
        hasDataReceivedListener: listenerCount > 0,
        listenerCount: listenerCount
      })
      
      if (listenerCount === 0) {
        console.error('❌❌❌ CRITICAL: DataReceived listener was NOT registered! ❌❌❌')
      }
      
      // Also register using string name as fallback (some versions might need this)
      try {
        newRoom.on('dataReceived', dataReceivedHandler)
        console.log('✅ Also registered DataReceived listener using string name')
      } catch (e) {
        console.warn('⚠️ Could not register DataReceived using string name:', e)
      }
      
      // Listen for connection errors
      newRoom.on(RoomEvent.Disconnected, (reason) => {
        console.log('Room disconnected:', reason)
        setIsConnected(false)
      })
      
      newRoom.on(RoomEvent.Connected, () => {
        console.log('Room connected successfully')
        console.log('Remote participants:', newRoom.remoteParticipants.size)
        // Log all remote participants
        newRoom.remoteParticipants.forEach((participant, identity) => {
          console.log(`  - Participant: ${identity}, tracks: ${participant.trackPublications.size}`)
        })
      })
      
      // Listen for when remote participants join (this might be the agent)
      newRoom.on(RoomEvent.ParticipantConnected, (participant) => {
        console.log(`Participant connected: ${participant.identity}`)
        console.log(`  - Tracks: ${participant.trackPublications.size}`)
      })
      
      await newRoom.connect(finalUrl, token)
      console.log('✅ Room connected successfully!')
      console.log('   Room name:', newRoom.name)
      console.log('   Local participant:', newRoom.localParticipant.identity)
      console.log('   Remote participants:', newRoom.remoteParticipants.size)
      
      // Log all remote participants
      newRoom.remoteParticipants.forEach((_participant, identity) => {
        console.log(`   - Remote participant: ${identity}`)
      })
      
      // Verify data channel is ready
      const finalListenerCount = newRoom.listenerCount(RoomEvent.DataReceived)
      console.log('🔍 Data channel status after connection:', {
        roomState: newRoom.state,
        isConnected: newRoom.state === 'connected',
        hasDataReceivedListener: finalListenerCount > 0,
        listenerCount: finalListenerCount,
        localParticipant: newRoom.localParticipant?.identity,
        remoteParticipants: newRoom.remoteParticipants.size
      })
      
      if (finalListenerCount === 0) {
        console.error('❌❌❌ CRITICAL: DataReceived listener was lost after connection! ❌❌❌')
        console.error('   Re-registering DataReceived listener...')
        newRoom.on(RoomEvent.DataReceived, dataReceivedHandler)
        console.log('   ✅ Re-registered DataReceived listener')
      }
      
      // Also set up listener again after connection as a safety measure
      newRoom.on(RoomEvent.DataReceived, dataReceivedHandler)
      console.log('✅ DataReceived listener re-registered after connection (safety measure)')
      
      // Verify listener is still attached
      const postConnectionListenerCount = newRoom.listenerCount(RoomEvent.DataReceived)
      console.log('🔍 Post-connection listener count:', postConnectionListenerCount)
      
      if (postConnectionListenerCount === 0) {
        console.error('❌❌❌ CRITICAL: DataReceived listener lost after connection! ❌❌❌')
        // Try to re-register one more time
        newRoom.on(RoomEvent.DataReceived, dataReceivedHandler)
        console.log('   ✅ Attempted to re-register listener')
      }
      
      // Test: Log whenever ANY room event fires to verify event system is working
      const testHandler = () => {
        console.log('🧪 Test: Room event system is working')
      }
      newRoom.on(RoomEvent.Connected, testHandler)
      
      // Test data channel by sending a test message
      console.log('🧪 Testing data channel by sending test message...')
      setTimeout(async () => {
        try {
          const testData = JSON.stringify({ type: 'test', message: 'Frontend data channel test', timestamp: Date.now() })
          const testBytes = new TextEncoder().encode(testData)
          
          // Try to send data to verify the channel works
          newRoom.localParticipant.publishData(testBytes, { reliable: true })
          console.log('   ✅ Test data sent from frontend')
          console.log('   📦 Test data:', testData)
        } catch (e: any) {
          console.error('   ❌ Failed to send test data:', e)
        }
      }, 2000) // Wait 2 seconds after connection
      
      // Monitor for data channel readiness
      console.log('🔍 Monitoring data channel...')
      const checkInterval = setInterval(() => {
        const count = newRoom.listenerCount(RoomEvent.DataReceived)
        console.log(`   📊 DataReceived listener count: ${count}`)
        if (count === 0) {
          console.warn('⚠️ DataReceived listener count is 0! Re-registering...')
          newRoom.on(RoomEvent.DataReceived, dataReceivedHandler)
        }
      }, 5000) // Check every 5 seconds
      
      // Clear interval when component unmounts
      setTimeout(() => clearInterval(checkInterval), 120000) // Stop after 2 minutes
      
      // Enable microphone after connection
      try {
        const localParticipant = newRoom.localParticipant
        if (!localParticipant) {
          throw new Error('Local participant not available')
        }
        
        await localParticipant.setMicrophoneEnabled(true)
        console.log('Microphone enabled')
        
        // Wait a bit for the track to be published
        await new Promise(resolve => setTimeout(resolve, 500))
        
        // Check if audio track is published (safely)
        try {
          const allPublications = Array.from(localParticipant.trackPublications.values())
          const audioPublications = allPublications.filter(pub => pub.kind === 'audio')
          if (audioPublications.length > 0) {
            console.log('Audio tracks published:', audioPublications.length)
            audioPublications.forEach((pub) => {
              if (pub.kind === 'audio') {
                console.log('Audio track:', pub.trackSid, 'enabled:', !pub.isMuted)
              }
            })
          } else {
            console.log('Audio tracks not yet available, will be published soon')
          }
        } catch (trackErr: any) {
          console.warn('Could not check audio tracks:', trackErr)
          // This is not critical, so we don't throw
        }
      } catch (micErr: any) {
        console.warn('Could not enable microphone:', micErr)
        const errorMsg = micErr?.message || micErr?.toString() || 'Unknown error'
        setError(`Microphone error: ${errorMsg}. You may need to grant permission again.`)
      }
      
      // Listen for track published events
      newRoom.on(RoomEvent.TrackPublished, (publication, participant) => {
        console.log('Track published:', publication.kind, 'by', participant.identity)
      })
      
      // Listen for track subscribed events
      newRoom.on(RoomEvent.TrackSubscribed, (track, _publication, participant) => {
        console.log('Track subscribed:', track.kind, 'from', participant.identity)
      })
      
      setRoom(newRoom)
      roomRef.current = newRoom // Keep ref in sync
      setIsConnected(true)
    } catch (err: any) {
      let errorMessage = 'Failed to connect'
      
      if (err.message) {
        errorMessage = err.message
      } else if (err.name === 'NotAllowedError') {
        errorMessage = 'Microphone permission denied. Please allow microphone access and try again.'
      } else if (err.name === 'NotFoundError') {
        errorMessage = 'No microphone found. Please connect a microphone.'
      }
      
      setError(errorMessage)
      console.error('Connection error:', err)
    }
  }

  const disconnect = async () => {
    if (room) {
      room.disconnect()
      setRoom(null)
      roomRef.current = null
      setIsConnected(false)
      setToolCalls([])
      setSummary(null)
    }
  }

  return (
    <div className="app">
      <div className="app-container">
        <header className="app-header">
          <h1>🎙️ SuperBryn Voice Agent</h1>
          <p>AI-Powered Appointment Booking Assistant</p>
        </header>

        {error && (
          <div className="error-message">
            <strong>⚠️ Error</strong>
            <div>{error}</div>
            {error.includes('permission') || error.includes('Permission') ? (
              <div style={{ marginTop: '15px', fontSize: '0.9rem' }}>
                <strong>How to fix:</strong>
                <ul>
                  <li>Click the lock/info icon in your browser's address bar</li>
                  <li>Find "Microphone" in the permissions list</li>
                  <li>Change it to "Allow"</li>
                  <li>Refresh the page and try again</li>
                </ul>
                <p style={{ marginTop: '10px', fontSize: '0.85rem', fontStyle: 'italic' }}>
                  Or go to: Chrome → Settings → Privacy → Site Settings → Microphone
                </p>
              </div>
            ) : null}
          </div>
        )}

        {!isConnected ? (
          <div className="connect-section">
            <button onClick={connectToRoom} className="connect-button">
              Start Voice Call
            </button>
          </div>
        ) : (
          <div className="call-section">
            <VoiceAgent room={room!} />
            
            <div className="call-controls">
              <ToolCallDisplay toolCalls={toolCalls} />
              <button onClick={disconnect} className="disconnect-button">
                End Call
              </button>
            </div>

            {summary && (
              <ConversationSummary summary={summary} />
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default App
