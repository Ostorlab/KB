The application streams audio and video (for example during a telehealth video visit) without giving the user a reliable,
on-screen or in-notification indication that the camera and microphone are actively streaming and may be recorded
server-side.

Two complementary transparency gaps are typically present:

- **No in-app recording/streaming indicator.** The media SDK emits recording lifecycle events (for example Twilio's
  `Room.Listener.onRecordingStarted` / `onRecordingStopped`), but the UI layer discards them — they fall into a
  catch-all `else` branch that only logs `"Unhandled RoomEvent"`. As a result, when the provider or the server starts
  server-side recording, the patient receives no on-screen indicator.

- **Unclear foreground notification.** The ongoing foreground-service notification (shown while the camera and
  microphone are streaming, including when the app is backgrounded) sets only `.setContentTitle(roomName)` with no
  `.setContentText(...)` describing the active streaming, and the notification channel is created with
  `NotificationManager.IMPORTANCE_LOW`. The displayed "room name" is a localized display label (for example
  `"Call with %1$s"` formatted from an unverified deep-link value) rather than a verifiable session identifier.

### Impact

The practical impact is reduced user awareness and the inability to independently confirm recording status or
session/provider identity. This is a transparency and defense-in-depth gap with potential recording-consent
implications, particularly in a medical context. It is rated **Low** because the absence of an indicator does not by
itself expose protected health data, and exploitation requires a separate spoofing vector to compound the
transparency gap.

### Example (vulnerable)

The recording events are emitted by the SDK but discarded by the view model, and the foreground notification carries
only a display label.

#### Kotlin

```kotlin
// RoomViewModel.kt — recording events fall into the unhandled catch-all
private fun observeRoomEvents() {
    roomEvents.onEach { roomEvent ->
        when (roomEvent) {
            is RoomEvent.Connecting -> { /* ... */ }
            is RoomEvent.Connected -> { /* ... */ }
            is RoomEvent.Disconnected, is RoomEvent.ConnectFailure -> showErrorDialog(roomEvent)
            else -> {
                // Currently unhandled RoomEvents (includes RecordingStarted/RecordingStopped)
                VideoChatAnalytics.logMessage("Unhandled RoomEvent: $roomEvent")
            }
        }
    }.launchIn(viewModelScope)
}
```

```kotlin
// RoomNotification.kt — bare foreground notification, no content text, low-importance channel
fun buildNotification(roomName: String): Notification =
    NotificationCompat.Builder(context, VIDEO_SERVICE_CHANNEL)
        .setSmallIcon(R.drawable.ic_camera_on)
        .setContentTitle(roomName)                 // display label only
        .setPriority(NotificationCompat.PRIORITY_DEFAULT)
        .setOngoing(true)
        .build()

// channel created with IMPORTANCE_LOW
NotificationChannel(VIDEO_SERVICE_CHANNEL, "Video Call", NotificationManager.IMPORTANCE_LOW).also {
    it.lockscreenVisibility = Notification.VISIBILITY_PUBLIC
}
```
