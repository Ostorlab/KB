## Recommendation

Never render server-authored error text verbatim to end users. Map known server error codes/names to localized client strings and fall back to a generic localized message for any unmapped server text.

### Immediate Mitigation

Remove the verbatim-rendering code paths in the view models. Replace `customMessageString = error.message`, `UiState.Error(error = error)`, and `UiState.Error(e)` (where the source is an `ApiException`/`RestApiException`) with localized resource strings keyed off the server error type:

```kotlin
// LoginUsernameViewModel.kt — replace the verbatim branches
error.containsError("PasswordResetRequiredException") ->
    UiState.Error(R.string.error_password_reset_required, showTime = null)
else -> UiState.Error(R.string.error_signing_in, showTime = null)
```

```kotlin
// StateOfResSelectionViewModel.kt — replace the verbatim branch
.onApiError { uiState.value = UiState.Error(R.string.error_saving) }
```

As a defense-in-depth guard, make the state holder's message resolver ignore any raw `customMessageString` originating from `ApiException`/`RestApiException` sources, so a future verbatim path cannot reach the UI.

### Permanent Fix

* Introduce an allow-list that maps known server error codes/names (for example `LegacyAuthMismatchException`, `PasswordResetRequiredException`, GraphQL `extensions.code` values) to localized client strings. Never construct an error UI state from raw `error.message`.
* Coordinate with the backend to return stable, machine-readable error codes rather than free-text messages.
* Add redaction so that any unmapped server message falls back to a generic localized string rather than the raw text.
* Add regression tests asserting that a server payload carrying an internal message produces a localized UI state (e.g. `UiState.Error(R.string.*)`), not the raw message. Add a dedicated test modeling a GraphQL `Error.message` payload and asserting the rendered UI string is the localized fallback, not the server text.

### Verification

1. Grep the repository for `customMessageString = error.message`, `UiState.Error(error = error)`, and `UiState.Error(e)` with an `ApiException`/`RestApiException` source; confirm zero remaining matches after the fix.
2. Confirm that assistive technology (e.g. TalkBack) announces the localized string rather than the raw server message.
