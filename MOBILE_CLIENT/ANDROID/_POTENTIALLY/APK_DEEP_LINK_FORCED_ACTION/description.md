# Android Deep Link Forced Action

The application declares one or more exported entry points reachable through deep links: an `<activity>`
with `android:exported="true"` (or an intent-filter that implicitly exports it) carrying an
`<intent-filter>` with a custom `android:scheme` and the `android.intent.category.BROWSABLE`
category. Because the host portion is frequently wildcarded (`android:host="*"`) and the
`DEFAULT` category is set, the operating system resolves `scheme://...` `VIEW` intents delivered
by `adb`, any other installed application, or a crafted web page directly into the activity
without presenting a chooser.

The risk arises when the deep-link entry point is the only boundary between an external caller
and a state-mutating sink. Two related sub-patterns must be reviewed:

1. **Forced-action execution.** Deep-link query parameters are bound into the destination's
   navigation arguments / saved state. If those parameters are consumed by code that invokes a
   state-mutating operation (for example a GraphQL mutation that marks a task complete, submits a
   workout, or confirms an action), an attacker can drive the signed-in user into a
   state-changing flow purely by delivering an intent. A silent forced action occurs when the
   mutation is reached directly from the deep-link handler or from a destination's `init` /
   `onStart` lifecycle without an explicit user interaction (such as a button tap).

2. **Mass assignment of the underlying mutation.** When the deep link or its destination builds a
   GraphQL mutation input from request data, attacker-supplied fields (`userId`, `programId`,
   `isVerified`, `completionDate`, `score`, etc.) may be persisted server-side, allowing the caller
   to act on behalf of another principal or to backdate compliance reporting. Mass assignment is a
   server-side trust question, but the client is the surface that transports the attacker-controlled
   fields, so both sides must be reviewed.

A static trace that reaches the deep-link handler and confirms it only performs navigation — and
that any state-mutating sink is gated behind explicit user interaction and the caller's own
identity — refutes the forced-action claim. A schema field-set proof that the candidate injected
fields are absent from the mutation input types, combined with typed input serialization that
cannot emit undeclared fields, refutes the mass-assignment claim. Until such a trace is complete,
an exported deep-link entry that can reach a mutation sink must be treated as a potential
vulnerability and verified dynamically.

### Example

```xml
<activity
    android:name=".ui.MainActivity"
    android:exported="true"
    android:launchMode="singleTask">
    <intent-filter>
        <data android:host="*" android:scheme="app" />
        <action android:name="android.intent.action.VIEW" />
        <category android:name="android.intent.category.DEFAULT" />
        <category android:name="android.intent.category.BROWSABLE" />
    </intent-filter>
</activity>
```
