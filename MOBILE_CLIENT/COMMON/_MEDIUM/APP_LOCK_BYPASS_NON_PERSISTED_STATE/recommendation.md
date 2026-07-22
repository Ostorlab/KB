Persist the lock-engagement flag (and a `locked` flag) across process death and read it synchronously before composing the authenticated navigation graph, so the lock is engaged by default on cold start until the server confirms the lock state.

### Immediate mitigation

Compose the lock overlay as the default view on cold start until the server confirms the lock state, so no authenticated navigation graph renders while the lock state is `Unknown`:

=== "Kotlin"
	```kotlin
	// Treat Unknown as locked at the UI layer.
	if (viewState.data.showPasscodeScreen || viewState.data.initialDestination.isEmpty()) {
	    AppLockedPasscodeScreen(viewModel = enterPasscodeViewModel)
	} else {
	    NavGraph(... startDestination = viewState.data.initialDestination)
	    LaunchedEffect(Unit) { onNavGraphReady() }
	}
	```

And route `Unknown` to the locked branch in the launch collector:

=== "Kotlin"
	```kotlin
	userLockedOut.collect {
	    when (it) {
	        UserLockedOut.ShowPinEntry, UserLockedOut.Unknown ->
	            viewState.value = MainViewData(initialDestination = "", showPasscodeScreen = true)
	        UserLockedOut.Unlocked ->
	            viewState.value = MainViewData(initialDestination = initialDestination)
	    }
	}
	```

### Permanent fix

Persist `hasPasscode` (and a `locked` flag) across process death and read it synchronously before composing the authenticated navigation graph:

=== "Kotlin"
	```kotlin
	// Persist and restore hasPasscode.
	var hasPasscode: Boolean = appSettings.hasPasscode // restored synchronously in init
	    set(value) {
	        field = value
	        appSettings.hasPasscode = value // persist
	        updateLockScreenState()
	    }
	```

Initialize the lock state based on the persisted flag so a passcode-enabled user starts locked:

=== "Kotlin"
	```kotlin
	val userLockedOut = MutableStateFlow(
	    if (hasPasscode) UserLockedOut.ShowPinEntry else UserLockedOut.Unlocked
	)
	```

### Verification

1. Sign in, set a passcode, populate the home screen cache, then background the application.
2. Force-stop / swipe-away the application from recents and relaunch it (cold start).
3. Capture the first frames: confirm the lock screen appears immediately and no authenticated home content renders before the lock.
4. Enter the passcode and confirm the home screen only then composes.
5. Repeat with an empty cache to confirm the lock still shows first regardless of cache state.
