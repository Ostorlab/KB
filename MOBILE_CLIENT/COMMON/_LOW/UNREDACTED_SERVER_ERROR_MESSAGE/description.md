# Unredacted Server Error Messages Rendered Verbatim to End Users

When a mobile application receives an error response from a backend service (REST or GraphQL), it must decide how to surface that failure to the user. Rendering the server-authored error text verbatim to the end user is an **information disclosure** weakness: the server message is not designed as user-facing copy and may embed internal implementation details that aid reconnaissance.

## Description

The application exposes the raw server error text to the user on one or more error code paths. Typically the data flow is:

1. A network layer throws an exception whose `message` getter returns the server-authored text unchanged. For REST this is the parsed `ApiError.message` field (and accompanying `errors[]` array of internal exception class names); for GraphQL it is `response.errors.first().message` per the GraphQL specification.
2. A view model constructs an error UI state from `error.message` (or the exception object itself) instead of mapping the server error to a localized client string.
3. A state holder stores that raw string as the message to render, with no allow-list mapping server error codes/names to localized strings and no redaction of unmapped text.
4. The UI renders the string verbatim in a visible control (for example a `Text` composable, a `Snackbar`, or a `Toast`) and frequently also announces it to assistive technologies via a `contentDescription`.

There is no sanitization hop between the thrown exception and the rendered text, so any future server change that emits a more descriptive message is auto-leaked.

## Impact

The disclosure is shown only to the application's own (authenticated) user, so the direct impact is limited. The realistic exposure is **reconnaissance-aiding information disclosure** rather than direct compromise. Per the GraphQL specification, `Error.message` is server-authored text and may include:

* Internal field names and enum values.
* Validation or database-derived messages (for example constraint names, column names, or SQL error fragments).
* Internal exception class names (e.g. `LegacyAuthMismatchException`, `PasswordResetRequiredException`) that reveal account-state or authentication-flow internals.

This information helps an attacker understand the backend schema, account states, and validation logic, which can support secondary attacks such as user enumeration or targeted parameter manipulation.

> Note: This weakness concerns **verbatim server-authored error text**, not JVM or server stack traces. A `message` getter that returns `response.errors.first().message` exposes server text, not `Throwable.stackTrace`. The "stack traces rendered to the user" phrasing is therefore not supported by this class of issue; only verbatim message rendering applies.

## Risk Rating

**Low.** The information is disclosed to the application's own user and is reconnaissance-aiding rather than directly destructive. Higher-impact exploitation (such as account enumeration) is tracked separately where applicable.

## References

* [CWE-209: Information Exposure Through an Error Message](https://cwe.mitre.org/data/definitions/209.html)
* [CWE-215: Information Exposure Through Debug Information](https://cwe.mitre.org/data/definitions/215.html)
