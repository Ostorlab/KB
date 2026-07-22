Add `FLAG_SECURE` to every `Activity` window that displays sensitive data, on every code path and build variant. Apply the flag in `onCreate`, before `setContent {}` draws any UI, so the protection is in place from the first rendered frame.

### Immediate mitigation

=== "Kotlin"
	```kotlin
	override fun onCreate(savedInstanceState: Bundle?) {
	    showOnLockScreen()
	    super.onCreate(savedInstanceState)
	    // Block screenshots, screen recording and MediaProjection of this window on every build variant.
	    window.setFlags(
	        WindowManager.LayoutParams.FLAG_SECURE,
	        WindowManager.LayoutParams.FLAG_SECURE,
	    )
	    // ... existing extras handling and setContent ...
	}
	```

Set the flag **unconditionally** — do not gate it on `BuildConfig.DEBUG`. Keep any existing keep-screen-on / allow-lock-while-screen-on logic; `FLAG_SECURE` is additive and compatible with `FLAG_KEEP_SCREEN_ON`, `FLAG_ALLOW_LOCK_WHILE_SCREEN_ON`, `setShowWhenLocked(true)` and `setTurnScreenOn(true)`.

### Permanent fix

Introduce a shared base `ComponentActivity` that sets `FLAG_SECURE` in `onCreate` on every build variant, and have every sensitive-data `Activity` extend it. This removes the per-`Activity` reliance on remembering to set the flag and prevents the same gap recurring for future Activities.

=== "Kotlin"
	```kotlin
	abstract class SecureComponentActivity : ComponentActivity() {
	    override fun onCreate(savedInstanceState: Bundle?) {
	        super.onCreate(savedInstanceState)
	        window.setFlags(
	            WindowManager.LayoutParams.FLAG_SECURE,
	            WindowManager.LayoutParams.FLAG_SECURE,
	        )
	    }
	}

	class IncomingCallActivity : SecureComponentActivity() { /* ... */ }
	class MainActivity : SecureComponentActivity() { /* ... */ }
	```

### Prevent regressions

Add an instrumentation test or a static check (lint / detekt / unit test) asserting that every `Activity` in the sensitive-data set sets `FLAG_SECURE` on its window in `onCreate` (for example assert `window.attributes.flags and FLAG_SECURE != 0`), so a new sensitive `Activity` cannot ship without the flag. A repository-wide search for `FLAG_SECURE` should return a match in every sensitive `Activity` (or the shared base class).
