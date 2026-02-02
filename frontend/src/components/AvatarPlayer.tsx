import React, { useEffect, useRef, useState } from 'react'
import { RemoteVideoTrack, Track } from 'livekit-client'
import './AvatarPlayer.css'

interface AvatarPlayerProps {
  videoTrack: RemoteVideoTrack | null
  isSpeaking: boolean
  avatarProvider?: 'tavus' | 'beyond-presence' | 'livekit-video' | 'none'
  // Tavus-specific props
  tavusReplicaId?: string
  tavusApiKey?: string
  // Beyond Presence-specific props
  beyondPresenceApiKey?: string
  beyondPresenceAvatarId?: string
}

/**
 * AvatarPlayer component that handles different avatar providers
 * - LiveKit Video: Uses video tracks from the agent
 * - Tavus: Integrates with Tavus API for avatar rendering
 * - Beyond Presence: Integrates with Beyond Presence API
 * - None: Fallback placeholder
 */
const AvatarPlayer: React.FC<AvatarPlayerProps> = ({
  videoTrack,
  isSpeaking,
  avatarProvider = 'livekit-video',
  tavusReplicaId,
  tavusApiKey,
  beyondPresenceApiKey,
  beyondPresenceAvatarId,
}) => {
  const videoRef = useRef<HTMLVideoElement>(null)
  const [avatarReady, setAvatarReady] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Handle LiveKit video track (works for livekit-video, tavus, and beyond-presence)
  // Tavus/Beyond Presence avatars publish video tracks through LiveKit
  useEffect(() => {
    // For Tavus/Beyond Presence, they also use LiveKit video tracks
    const shouldUseVideoTrack = avatarProvider === 'livekit-video' || 
                                avatarProvider === 'tavus' || 
                                avatarProvider === 'beyond-presence'
    
    if (!shouldUseVideoTrack || !videoTrack) {
      console.log('AvatarPlayer: Not using video track', { avatarProvider, hasVideoTrack: !!videoTrack })
      return
    }

    const videoElement = videoRef.current
    if (!videoElement) {
      console.warn('AvatarPlayer: Video element not available')
      return
    }

    console.log('AvatarPlayer: Attaching video track to element', {
      trackId: videoTrack.sid,
      kind: videoTrack.kind,
      isMuted: videoTrack.isMuted,
    })

    try {
      // Attach the track to the video element
      videoTrack.attach(videoElement)
      setAvatarReady(true)
      setError(null)
      console.log('AvatarPlayer: Video track attached successfully')

      // Handle video track events
      const handleStarted = () => {
        console.log('AvatarPlayer: Video track started')
        setAvatarReady(true)
      }

      const handleEnded = () => {
        console.log('AvatarPlayer: Video track ended')
        setAvatarReady(false)
      }

      const handleMuted = () => {
        console.log('AvatarPlayer: Video track muted')
      }

      const handleUnmuted = () => {
        console.log('AvatarPlayer: Video track unmuted')
      }

      videoTrack.on('started', handleStarted)
      videoTrack.on('ended', handleEnded)
      videoTrack.on('muted', handleMuted)
      videoTrack.on('unmuted', handleUnmuted)

      // Force play
      videoElement.play().catch((err: any) => {
        console.warn('AvatarPlayer: Error playing video:', err)
      })

      return () => {
        console.log('AvatarPlayer: Cleaning up video track')
        videoTrack.off('started', handleStarted)
        videoTrack.off('ended', handleEnded)
        videoTrack.off('muted', handleMuted)
        videoTrack.off('unmuted', handleUnmuted)
        videoTrack.detach()
      }
    } catch (err: any) {
      console.error('AvatarPlayer: Error attaching video track:', err)
      setError(`Failed to load avatar video: ${err.message}`)
    }
  }, [videoTrack, avatarProvider])

  // Handle Tavus integration
  useEffect(() => {
    if (avatarProvider !== 'tavus') return

    // Tavus integration would go here
    // For now, we'll use a placeholder until Tavus SDK is available
    // When implementing, you would:
    // 1. Initialize Tavus SDK with apiKey and replicaId
    // 2. Connect to Tavus streaming API
    // 3. Render avatar video in the container
    // 4. Sync with audio track if provided
    console.log('Tavus avatar integration - replica ID:', tavusReplicaId)
    setAvatarReady(true)
  }, [avatarProvider, tavusReplicaId, tavusApiKey])

  // Handle Beyond Presence integration
  useEffect(() => {
    if (avatarProvider !== 'beyond-presence') return

    // Beyond Presence integration would go here
    // When implementing, you would:
    // 1. Initialize Beyond Presence SDK with apiKey and avatarId
    // 2. Connect to their streaming API
    // 3. Render avatar video in the container
    // 4. Sync with audio track if provided
    console.log('Beyond Presence avatar integration - avatar ID:', beyondPresenceAvatarId)
    setAvatarReady(true)
  }, [avatarProvider, beyondPresenceApiKey, beyondPresenceAvatarId])

  // Render based on provider
  // For Tavus/Beyond Presence with LiveKit integration, they publish video tracks
  // So we use the same video rendering as livekit-video
  if (videoTrack && (avatarProvider === 'livekit-video' || avatarProvider === 'tavus' || avatarProvider === 'beyond-presence')) {
    return (
      <div className="avatar-player-container">
        <video
          ref={videoRef}
          className={`avatar-video ${isSpeaking ? 'speaking' : ''} ${avatarReady ? 'ready' : 'loading'}`}
          autoPlay
          playsInline
          muted={false}
        />
        {!avatarReady && (
          <div className="avatar-loading">
            <div className="spinner"></div>
            <span>Loading avatar...</span>
          </div>
        )}
        {error && <div className="avatar-error">{error}</div>}
      </div>
    )
  }

  // Placeholder when no video track is available yet
  if (avatarProvider === 'tavus') {
    return (
      <div className="avatar-player-container">
        <div className="avatar-tavus">
          <div className="avatar-placeholder">
            <span>🎭</span>
            <p>Tavus Avatar</p>
            {tavusReplicaId && <small>Replica: {tavusReplicaId}</small>}
            {!videoTrack && <small style={{display: 'block', marginTop: '8px', color: '#666'}}>Waiting for video...</small>}
          </div>
        </div>
      </div>
    )
  }

  if (avatarProvider === 'beyond-presence') {
    return (
      <div className="avatar-player-container">
        <div className="avatar-beyond-presence">
          <div className="avatar-placeholder">
            <span>👤</span>
            <p>Beyond Presence Avatar</p>
            {beyondPresenceAvatarId && <small>Avatar: {beyondPresenceAvatarId}</small>}
            {!videoTrack && <small style={{display: 'block', marginTop: '8px', color: '#666'}}>Waiting for video...</small>}
          </div>
        </div>
      </div>
    )
  }

  // Fallback placeholder
  return (
    <div className="avatar-player-container">
      <div className={`avatar-placeholder ${isSpeaking ? 'speaking' : ''}`}>
        <span>🤖</span>
      </div>
    </div>
  )
}

export default AvatarPlayer
