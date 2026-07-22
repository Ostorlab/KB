To reduce the risk of forced-action execution and mass assignment through deep links, apply the
following controls:

- Prefer Android App Links (verified `http`/`https` deep links with `autoVerify`) over custom
  schemes. Custom schemes with a wildcard host and the `BROWSABLE` category accept intents from any
  installed application, `adb`, and crafted web pages, so they should be avoided for
  state-changing entry points.
- Do not bind attacker-controlled entity identifiers from deep-link query parameters into
  state-mutating sinks. Select the targeted resource from the authenticated principal's own data
  (for example the signed-in user's own task list), so a deep link can only act on resources the
  caller already owns.
- Gate deep-link argument consumption behind an authentication check. Drop the deep-link arguments
  (early return) when no valid authenticated identity exists, so the link cannot trigger any
  navigation or mutation for an unauthenticated user.
- Never invoke a state-mutating sink (such as a GraphQL mutation) directly from a deep-link
  handler, a destination's `init`, `onStart`, or a `LaunchedEffect`. Reach the sink only through
  an explicit user interaction (for example a button tap on the destination screen) so the action
  is never silent.
- For client-supplied timestamps used for compliance dating, do not trust a client-provided
  value for the persisted time; clamp or override it with server time so a backdated
  `responseTime` cannot be recorded.
- For GraphQL mutations reached from a deep-link flow, construct mutation inputs with typed
  input-object constructors that serialize only declared fields. Confirm the candidate
  attacker-supplied fields (`userId`, `programId`, `isVerified`, `completionDate`, `score`) do
  not exist on the relevant schema input types, so the client cannot transport them and a
  spec-compliant server rejects them before execution.
- Confirm dynamically that delivering the deep link lands on the destination screen without
  emitting any mutation traffic until the user explicitly confirms, and that a raw GraphQL request
  appending extra input fields is rejected by the server.
