import React, { useEffect, useRef, useState } from 'react'
import { Room, LocalAudioTrack, RemoteAudioTrack, RemoteVideoTrack, Track, RemoteParticipant } from 'livekit-client'
import AvatarPlayer from './AvatarPlayer'
import './VoiceAgent.css'

interface VoiceAgentProps {
  room: Room
}

const VoiceAgent: React.FC<VoiceAgentProps> = ({ room }) => {
  const [isMuted, setIsMuted] = useState(false)
  const [isSpeaking, setIsSpeaking] = useState(false)
  const [videoTrack, setVideoTrack] = useState<RemoteVideoTrack | null>(null)
  const audioRef = useRef<HTMLAudioElement>(null)
  
  // Avatar configuration from environment variables
  const avatarProvider = (import.meta.env.VITE_AVATAR_PROVIDER || 'livekit-video') as 'tavus' | 'beyond-presence' | 'livekit-video' | 'none'
  const tavusReplicaId = import.meta.env.VITE_TAVUS_REPLICA_ID
  const tavusApiKey = import.meta.env.VITE_TAVUS_API_KEY
  const beyondPresenceApiKey = import.meta.env.VITE_BEYOND_PRESENCE_API_KEY
  const beyondPresenceAvatarId = import.meta.env.VITE_BEYOND_PRESENCE_AVATAR_ID

  useEffect(() => {
    // Set up audio and video tracks
    const setupTracks = () => {
      if (!audioRef.current) return

      const handleTrackSubscribed = (track: Track, publication: any, participant: RemoteParticipant) => {
        console.log(`Track subscribed: ${track.kind} from ${participant.identity}`)
        
        if (track.kind === Track.Kind.Audio) {
          const audioElement = audioRef.current
          if (audioElement) {
            track.attach(audioElement)
            
            // Detect speaking
            if (track instanceof RemoteAudioTrack) {
              track.on('started', () => {
                console.log('Agent started speaking')
                setIsSpeaking(true)
              })
              track.on('stopped', () => {
                console.log('Agent stopped speaking')
                setIsSpeaking(false)
              })
              
              // Also detect audio level changes for more accurate speaking detection
              track.on('volumeLevelChanged', (level: number) => {
                setIsSpeaking(level > 0.01) // Threshold for speaking detection
              })
            }
          }
        } else if (track.kind === Track.Kind.Video) {
          // Handle video track for avatar
          // For Tavus/Beyond Presence, the avatar joins as a separate participant
          // For direct video publishing, it comes from the agent participant
          if (track instanceof RemoteVideoTrack) {
            console.log(`Video track received from ${participant.identity}`)
            setVideoTrack(track)
            
            track.on('started', () => {
              console.log('Avatar video started')
            })
            
            track.on('ended', () => {
              console.log('Avatar video ended')
              setVideoTrack(null)
            })
          }
        }
      }

      const handleTrackUnsubscribed = (track: Track) => {
        if (track.kind === Track.Kind.Audio) {
          track.detach()
        } else if (track.kind === Track.Kind.Video) {
          if (track instanceof RemoteVideoTrack) {
            track.detach()
            setVideoTrack(null)
          }
        }
      }

      // Helper to find and subscribe to video tracks from any participant
      const findAndSubscribeToVideoTracks = () => {
        console.log(`🔍 Searching for video tracks across ${room.remoteParticipants.size} participants`)
        let videoTracksFound = 0
        
        room.remoteParticipants.forEach((participant) => {
          console.log(`Checking participant: ${participant.identity}`)
          
          // Log all track publications for debugging
          const allPubs = Array.from(participant.trackPublications.values())
          const videoPubs = allPubs.filter(pub => pub.kind === Track.Kind.Video)
          const audioPubs = allPubs.filter(pub => pub.kind === Track.Kind.Audio)
          
          console.log(`  📊 ${participant.identity}: ${videoPubs.length} video, ${audioPubs.length} audio publications`)
          
          // Check for Beyond Presence avatar
          if (participant.identity === 'bey-avatar-agent') {
            console.log('✅ Found Beyond Presence avatar participant!')
          }
          
          participant.trackPublications.forEach((publication) => {
            if (publication.kind === Track.Kind.Video) {
              videoTracksFound++
              const isSubscribed = publication.isSubscribed
              const hasTrack = !!publication.track
              console.log(`  🎥 Video publication from ${participant.identity}: subscribed=${isSubscribed}, hasTrack=${hasTrack}`)
              
              if (publication.track) {
                // Track already subscribed
                console.log(`  ✅ Video track already available from ${participant.identity}`)
                handleTrackSubscribed(publication.track, publication, participant)
              } else {
                // Track not subscribed yet, subscribe to it
                console.log(`  🔄 Subscribing to video track from ${participant.identity}...`)
                publication.setSubscribed(true)
              }
            }
          })
        })
        
        if (videoTracksFound === 0) {
          console.warn('⚠️  No video tracks found! Expected avatar participant (bey-avatar-agent) may not have joined yet.')
          console.warn('   Check backend logs for avatar session startup messages.')
        }
      }

      // Subscribe to existing tracks
      findAndSubscribeToVideoTracks()

      // Store handler references so we can remove them later
      const handleParticipantConnected = (participant: RemoteParticipant) => {
        console.log(`Participant connected: ${participant.identity}`)
        if (participant.identity === 'bey-avatar-agent') {
          console.log('✅ Beyond Presence avatar participant joined!')
        }
        // Check for video tracks when new participant joins
        findAndSubscribeToVideoTracks()
      }

      const handleTrackPublished = (publication: any, participant: RemoteParticipant) => {
        console.log(`📡 Track published: ${publication.kind} from ${participant.identity}`)
        if (publication.kind === Track.Kind.Video) {
          console.log(`🎥 Video track published from ${participant.identity}, subscribing...`)
          if (participant.identity === 'bey-avatar-agent') {
            console.log('✅ Beyond Presence avatar video track published!')
          }
          publication.setSubscribed(true)
        }
      }

      // Listen for new participants (avatar might join after agent)
      room.on('participantConnected', handleParticipantConnected)

      // Listen for track published events (before subscription)
      room.on('trackPublished', handleTrackPublished)
      
      // Listen for new tracks
      room.on('trackSubscribed', handleTrackSubscribed)
      room.on('trackUnsubscribed', handleTrackUnsubscribed)
      
      // Return cleanup function
      return () => {
        room.off('participantConnected', handleParticipantConnected)
        room.off('trackPublished', handleTrackPublished)
        room.off('trackSubscribed', handleTrackSubscribed)
        room.off('trackUnsubscribed', handleTrackUnsubscribed)
      }
    }

    const cleanup = setupTracks()

    return () => {
      // Call the cleanup function returned by setupTracks
      if (cleanup) {
        cleanup()
      }
      if (videoTrack) {
        videoTrack.detach()
        setVideoTrack(null)
      }
    }
  }, [room, videoTrack])

  const toggleMute = async () => {
    if (isMuted) {
      await room.localParticipant.setMicrophoneEnabled(true)
      setIsMuted(false)
    } else {
      await room.localParticipant.setMicrophoneEnabled(false)
      setIsMuted(true)
    }
  }

  return (
    <div className="voice-agent">
      <div className="avatar-container">
        <div className={`avatar-wrapper ${isSpeaking ? 'speaking' : ''}`}>
          <AvatarPlayer
            videoTrack={videoTrack}
            isSpeaking={isSpeaking}
            avatarProvider={avatarProvider}
            tavusReplicaId={tavusReplicaId}
            tavusApiKey={tavusApiKey}
            beyondPresenceApiKey={beyondPresenceApiKey}
            beyondPresenceAvatarId={beyondPresenceAvatarId}
          />
          {isSpeaking && <div className="speaking-indicator"></div>}
        </div>
        <div className="avatar-status">
          {isSpeaking ? 'Speaking...' : 'Listening...'}
        </div>
        {!videoTrack && (avatarProvider === 'tavus' || avatarProvider === 'beyond-presence') && (
          <div className="avatar-info">
            <small>
              Waiting for {avatarProvider === 'tavus' ? 'Tavus' : 'Beyond Presence'} avatar video...
            </small>
          </div>
        )}
      </div>

      <div className="audio-controls">
        <audio ref={audioRef} autoPlay />
        <button
          onClick={toggleMute}
          className={`mute-button ${isMuted ? 'muted' : ''}`}
        >
          {isMuted ? '🔇 Unmute' : '🎤 Mute'}
        </button>
      </div>
    </div>
  )
}

export default VoiceAgent
