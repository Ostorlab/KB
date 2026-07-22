Microphone and camera capture in the application is effectively gated behind runtime permission checks. Although the manifest may declare the install-time, auto-granted `FOREGROUND_SERVICE_MICROPHONE` and `FOREGROUND_SERVICE_CAMERA` permissions, actual audio and video capture only proceeds after the runtime permissions `RECORD_AUDIO`, `CAMERA` (and `POST_NOTIFICATIONS` on Android 13+) have been explicitly granted by the user.

The application verifies the runtime permissions before connecting to the media backend, and a foreground service of type `camera|microphone` is only started from a successful connection callback rather than directly from a user action such as accepting an incoming call. This means that no silent microphone or camera capture can occur without an explicit, runtime-granted permission, and that the camera/microphone foreground-service notification appears only after the media room is connected.

An example of the secure ordering is shown below:

```kotlin
fun checkPermissions(): Boolean {
    val cameraGranted = ContextCompat.checkSelfPermission(
        context, Manifest.permission.CAMERA,
    ) == PackageManager.PERMISSION_GRANTED
    val micGranted = ContextCompat.checkSelfPermission(
        context, Manifest.permission.RECORD_AUDIO,
    ) == PackageManager.PERMISSION_GRANTED
    return cameraGranted && micGranted
}

fun connectToRoom() {
    if (checkPermissions().not()) {
        // Surface the runtime permission prompt; do NOT connect or capture yet.
        requestPermissions(arrayOf(CAMERA, RECORD_AUDIO), REQUEST_CODE)
        return
    }
    roomManager.connect(identity = providerId, roomName = roomName)
}

// In the media Room.Listener callback, only invoked after a successful token + room connect:
override fun onConnected(room: Room) {
    VideoService.startService(context)
}
```

This is an effective control. The residual risk is limited to social engineering, where a victim tricked by a spoofed call voluntarily grants the runtime camera and microphone permissions. The runtime gate itself is correctly implemented and prevents unauthorised or silent capture.
