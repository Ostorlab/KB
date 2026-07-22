`FLAG_SECURE` (`WindowManager.LayoutParams.FLAG_SECURE`) is a **per-`Window`** flag. When it is set on an `Activity`'s `Window`, the Android platform (WindowManager / SurfaceFlinger) returns a black/empty bitmap for that window to `MediaProjection`, `screencap` (e.g. `adb shell screencap`, `screenrecord`) and any `SurfaceView`-mirroring / `VirtualDisplay` consumer, blocks or blackens screenshots taken with the hardware screenshot key combination or screenshot APIs, and hides the window's content in the recent-apps / overview (Recents) thumbnail.

Because the flag is **per-Window**, an `Activity` window that does **not** set it remains fully capturable even when another `Activity`'s window in the same application sets it. Coverage must therefore be evaluated independently for every `Activity` window that renders sensitive data — there is no inheritance: each `Activity` extends a framework base class (for example `androidx.activity.ComponentActivity`) directly, so a flag applied in one `Activity`'s `onCreate` does not propagate to any other `Activity`.

This vulnerability is raised when an `Activity` that displays sensitive data (for example a lock-screen / incoming-call / telehealth window that renders a caller or provider name and identifier, or any window presenting PHI, PII, credentials, financial or care-team data) never calls `window.setFlags(FLAG_SECURE, FLAG_SECURE)` (nor `window.addFlags(FLAG_SECURE)`) on any code path, including the production release build. Such a window is capturable on every build variant — including a non-debuggable, release-signed production build shipped via Google Play — by an external capture mechanism: the device's own stock screen recorder or screenshot key combination, `adb shell screencap` on a debuggable build, or a `MediaProjection` session started by a co-resident application after the user grants consent. No rooted device, debugger attach, or frida instrumentation is required.

The exposure is often introduced when an application protects its main `Activity` with `FLAG_SECURE` but forgets to protect a *separate* `Activity` window — for instance a lock-screen `Activity` declared in the manifest with `android:showOnLockScreen="true"` and `android:exported="true"` that draws sensitive content into its own `ComponentActivity` window via `setContent {}`. That separate window only receives unrelated flags such as `FLAG_KEEP_SCREEN_ON` and `FLAG_ALLOW_LOCK_WHILE_SCREEN_ON` (or uses `setShowWhenLocked(true)` / `setTurnScreenOn(true)` on Android O_MR1+) and never receives `FLAG_SECURE`.

A common, related manifestation is gating `FLAG_SECURE` behind a debug guard:

=== "Kotlin"
	```kotlin
	if (!BuildConfig.DEBUG) {
	    window.setFlags(
	        WindowManager.LayoutParams.FLAG_SECURE,
	        WindowManager.LayoutParams.FLAG_SECURE,
	    )
	}
	```

While AGP only sets `BuildConfig.DEBUG = true` for the literal `debug` build type (so this guard still protects custom build types such as `staging`, `prod` and `release`), the guard leaves the `debug` build variant unprotected and signals an intent to allow screen capture on at least one variant. Any `Activity` that renders sensitive data should set `FLAG_SECURE` unconditionally rather than gating it on the build variant.
