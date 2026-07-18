# Mobile Companion Strategy

The IdeasOS mobile strategy focuses on **high-speed capture and synchronization** rather than heavy-duty code editing. The primary objective is to allow users to quickly capture voice memos, take photos of sketches or whiteboards, review agent progress notifications, and command active workflows.

---

## 1. Responsive Progressive Web App (PWA)

To avoid Apple App Store and Google Play Store licensing friction and preserve the open-source spirit, IdeasOS implements a responsive **Progressive Web App (PWA)** built on React and Vite.

### Core PWA Manifest Properties
```json
{
  "short_name": "IdeasOS",
  "name": "Ideas Operating System for Ideas Mobile",
  "icons": [
    {
      "src": "favicon.ico",
      "sizes": "64x64 32x32 24x24 16x16",
      "type": "image/x-icon"
    },
    {
      "src": "logo192.png",
      "type": "image/png",
      "sizes": "192x192"
    },
    {
      "src": "logo512.png",
      "type": "image/png",
      "sizes": "512x512"
    }
  ],
  "start_url": ".",
  "display": "standalone",
  "theme_color": "#020408",
  "background_color": "#020408"
}
```

---

## 2. SQLite-Based Offline Mobile Synchronization

The mobile client leverages **Wa-SQLite** (WebAssembly-compiled SQLite running inside the mobile browser's Origin Private File System).

- **Offline Transaction Log**: When a user records a voice node in a subway tunnel, the metadata is saved to the local mobile SQLite database.
- **Sync Protocol**: When network connectivity is restored:
  - The PWA Service Worker triggers a synchronization event.
  - It sends incremental transaction logs (represented as JSON CRDT packets) back to the desktop's API gateway endpoint.

---

## 3. Mobile Voice Capture Transcription

Capture is optimized for voice notes, which is the fastest way to record ideas on the move.

1. **Local Record**: The UI captures raw audio input via the HTML5 `MediaRecorder` API using the AAC/OPUS codec.
2. **Transcription Routing**:
   - **Local fallback**: If connected to a desktop machine on the local network, the client posts the raw audio payload to the desktop FastAPI's `/api/v1/inbox/ingest` endpoint for local Whisper transcription.
   - **Offline processing**: If offline, the client buffers the audio file in IndexedDB. Once online, the file is synced and transcribed.

---

## 4. Mobile Notification Hub

Mobile users receive push notifications regarding agent milestones using the **Web Push API** (configured without Firebase using native VAPID keys):

- **Milestone Reached**: *"Research Agent completed ArXiv analysis on your project. Gaps identified: 3."*
- **Action Required**: *"AI Debate Room has generated two options for auth config. Click here to select one."*
- **Test Output**: *"Deployment build completed successfully. View live layout demo."*
