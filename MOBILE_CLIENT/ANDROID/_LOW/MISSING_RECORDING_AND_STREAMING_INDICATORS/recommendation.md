Surface recording/streaming status to the user and make the foreground notification unambiguous while the camera and
microphone are actively streaming.

### Immediate mitigation

- Add explicit `when` arms for the recording lifecycle events in the view model so they update view state and emit a
  view effect the UI layer can react to, instead of falling into the unhandled catch-all.
- Add a clearly visible, non-dismissible on-screen recording indicator (for example a red dot plus a localized
  "Recording" label) bound to that state.
- Update the foreground notification to include `.setContentText(...)` describing active camera/microphone
  streaming and, when recording is active, that fact. Consider raising the channel to `IMPORTANCE_DEFAULT` while a
  visit is live so the user is reliably notified.
- For session verification, surface the real room identifier (or a server-issued short verification code) in a
  confirmable UI element rather than relying only on the display label derived from an unverified value.

### Code examples

#### Kotlin

```kotlin
// RoomViewModel.kt — extend the when block
is RoomEvent.RecordingStarted -> {
    updateState { it.copy(isRecording = true) }
    action { sendEvent { RoomViewEffect.RecordingStarted } }
}
is RoomEvent.RecordingStopped -> {
    updateState { it.copy(isRecording = false) }
    action { sendEvent { RoomViewEffect.RecordingStopped } }
}
```

```kotlin
// RoomNotification.kt — make streaming/recording status explicit
NotificationCompat.Builder(context, VIDEO_SERVICE_CHANNEL)
    .setSmallIcon(R.drawable.ic_camera_on)
    .setContentTitle(roomName)
    .setContentText(context.getString(R.string.notification_streaming_active))
    .setCategory(NotificationCompat.CATEGORY_CALL)
    .setPriority(NotificationCompat.PRIORITY_DEFAULT)
    .setOngoing(true)
    .build()
```
