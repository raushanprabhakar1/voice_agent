/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_LIVEKIT_URL: string
  readonly VITE_AVATAR_PROVIDER: string
  readonly VITE_TAVUS_REPLICA_ID?: string
  readonly VITE_TAVUS_API_KEY?: string
  readonly VITE_BEYOND_PRESENCE_API_KEY?: string
  readonly VITE_BEYOND_PRESENCE_AVATAR_ID?: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
