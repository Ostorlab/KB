The application performs client-side passcode (PIN) validation but no client-side brute-force protection primitive was detected. Passcodes are typically short numeric PINs (a 4-digit PIN offers only 10,000 possibilities), so without any client-side attempt counter, max-failures lockout, cooldown, exponential backoff or rate limiting, the local UI lets the user retry wrong passcodes with no incremental penalty.

This is a defense-in-depth gap on the client. The actual feasibility of brute-forcing the passcode depends on the server-side resolver that validates the passcode (rate limiting, lockout and constant-time comparison). The server implementation is not part of the mobile application and cannot be verified statically, hence the finding is rated `potentially` pending runtime confirmation of the server throttling behaviour.

### Android

A typical vulnerable implementation verifies the passcode with a single network call and, on failure, simply resets the UI so the user can immediately retry. There is no attempt counter, no lockout state and no cooldown:

=== "Kotlin"
	```kotlin
	fun enterPasscode(newPasscode: String) {
	    viewModelScope.launch {
	        passcodeRepository.isPasscodeValid(newPasscode)
	            .collect { isValid ->
	                if (isValid) {
	                    processPasscodeMatches()
	                } else {
	                    uiState.value = UiState.Error(R.string.invalid_passcode)
	                    viewState.value = viewData.copy(isCorrect = false)
	                }
	            }
	    }
	}
	```

The small passcode space combined with no client-side throttling lowers the bar for an exhaustive search whenever the server-side resolver is permissive.
