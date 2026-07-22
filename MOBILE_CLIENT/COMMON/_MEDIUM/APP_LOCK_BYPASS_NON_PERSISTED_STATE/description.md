A client-side app lock (passcode, PIN, or biometric re-prompt) is a secondary gate layered on top of an already-authenticated session to protect sensitive data such as cached health, financial, or personally identifiable information. The gate is only effective if it is engaged before any protected content is composed and rendered.

This vulnerability occurs when the flag that engages the lock (for example `hasPasscode`) and the runtime lock state (for example `userLockedOut`) are held purely in memory and are not persisted across process death. On a force-stop and relaunch (cold start) of a signed-in device, persisted identity such as an OAuth token and user state is restored, so the application routes to the authenticated home screen. However, the in-memory lock state cannot be restored: it initializes to a default or `Unknown` value that the launch logic treats as `Unlocked`, so the authenticated UI (including cache-first reads of protected data) composes and renders before the lock is re-engaged by the asynchronous server response that restores the `hasPasscode` flag.

An attacker with brief physical possession of a locked device can therefore force-stop and relaunch the application to read cached authenticated content on each cold start. The exposure window is bounded by the latency of the asynchronous lock-restoring call (cache-first emissions are fast but non-zero, while the network path takes seconds), which is why the impact is rated Medium rather than High; the lock-bypass mechanism itself is deterministic on every cold start.

### Root cause

- The lock state is a purely in-memory reactive value initialized to a default/`Unknown` state:

=== "Kotlin"
	```kotlin
	// The lock state is not persisted and starts at Unknown on every cold start.
	val userLockedOut = MutableStateFlow(UserLockedOut.Unknown)

	var hasPasscode: Boolean = false
	    set(value) {
	        field = value
	        updateLockScreenState() // no disk write; the flag is lost on process death
	    }
	```

- The launch collector treats `Unknown` through the same branch as `Unlocked`, producing a view state that drives the authenticated navigation graph with the lock overlay disabled:

=== "Kotlin"
	```kotlin
	userLockedOut.collect {
	    when (it) {
	        UserLockedOut.ShowPinEntry ->
	            viewState.value = MainViewData(initialDestination = "", showPasscodeScreen = true)
	        else -> // Unknown falls through here and is indistinguishable from Unlocked
	            viewState.value = MainViewData(initialDestination = initialDestination) // showPasscodeScreen = false
	    }
	}
	```

- The authenticated navigation graph is composed as soon as the initial destination is non-empty, and the lock overlay is composed only afterwards when `showPasscodeScreen` becomes `true`. The asynchronous call that restores `hasPasscode` (and therefore flips the state to `ShowPinEntry`) runs concurrently and completes after the cache-first home screen has already rendered:

=== "Kotlin"
	```kotlin
	// Authenticated graph composes first.
	if (viewState.data.initialDestination.isNotEmpty()) {
	    NavGraph(startDestination = viewState.data.initialDestination)
	}
	// Lock overlay composes only once the async flag is restored.
	if (viewState.data.showPasscodeScreen) {
	    AppLockedPasscodeScreen(...)
	}
	```

### Exploitation

Reproduction requires only brief physical access to a signed-in, passcode-locked device:

1. Force-stop or swipe-away the application from the recent apps list. This kills the process but does **not** clear persisted identity (OAuth token, user state) stored in shared/encrypted preferences.
2. Relaunch the application icon (cold start). Persisted identity is restored, so the initial destination resolves to the authenticated home screen, while the in-memory lock state emits `Unknown` and is treated as `Unlocked`.
3. The authenticated home screen composes and renders cached protected content (cache-first reads) without the lock overlay for the duration of the lock-restoring call's first-emission latency.
4. Once the asynchronous call restores `hasPasscode`, the state flips to `ShowPinEntry` and recomposition replaces the authenticated graph with the lock screen.

The amount of content visible during the window is runtime- and cache-dependent, but the lock-bypass mechanism itself is deterministic on every cold start.
