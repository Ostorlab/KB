Enforce a client-side attempt counter with exponential backoff that disables the keypad after a number of wrong passcode attempts, and surface a "too many attempts" state to the user.

=== "Kotlin"
	```kotlin
	private var wrongAttemptCount = 0

	fun enterPasscode(newPasscode: String) {
	    if (isKeypadLockedOut()) {
	        uiState.value = UiState.Error(R.string.too_many_attempts)
	        return
	    }
	    viewModelScope.launch {
	        passcodeRepository.isPasscodeValid(newPasscode)
	            .collect { isValid ->
	                if (isValid) {
	                    wrongAttemptCount = 0
	                    processPasscodeMatches()
	                } else {
	                    wrongAttemptCount += 1
	                    val backoffSeconds = min(2.0.pow(wrongAttemptCount).toLong(), 60)
	                    startKeypadLockout(backoffSeconds)
	                    uiState.value = UiState.Error(R.string.invalid_passcode)
	                }
	            }
	    }
	}
	```

This lowers the brute-force bar on the client even if the server is permissive.

For a permanent fix, the server-side passcode resolver must enforce rate limiting, lockout and constant-time comparison so that an exhaustive passcode search is infeasible within the lockout window. Complement this by migrating the app lock from a short numeric PIN to a higher-entropy secret or to `BiometricPrompt`, which removes brute-force feasibility regardless of throttling.
