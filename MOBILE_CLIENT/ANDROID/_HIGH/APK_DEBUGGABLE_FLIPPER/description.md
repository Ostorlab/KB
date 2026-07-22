A debuggable Android application (`android:debuggable="true"` in the merged `AndroidManifest.xml`) that ships Flipper debugging instrumentation exposes sensitive data to any party with local USB/ADB access, without root and without additional permissions.

The `android:debuggable` attribute enables JDWP debugging and `adb shell run-as <package>` access to the application private data directory. When Flipper is also packaged into the build, the desktop Flipper client can additionally inspect:

* **Network traffic** — Flipper's network interceptor (typically added as the last application interceptor, after the interceptor that injects the `Authorization` header) captures the final outgoing request, including live `Authorization: Bearer <token>` headers, and the decompressed response bodies. For applications exchanging PHI or other sensitive data over GraphQL/REST, the full response payloads are captured.
* **SQLite databases** — `DatabasesFlipperPlugin` exposes the application's databases, including normalized GraphQL cache databases that persist PHI.
* **Shared preferences** — `SharedPreferencesFlipperPlugin` exposes preference entries read through the `SharedPreferences` API, including values that are encrypted at rest but decrypted in-process (e.g. OAuth tokens) and plaintext PII (e.g. email, user identifiers).

A debuggable build also typically skips screen-capture protections gated on a debug flag, so PHI rendered on screen can be screenshotted or recorded.

The combination is materially worse than a debuggable build alone: Flipper turns the debuggable surface into a structured, point-and-click exfiltration channel for live credentials and PHI. The exposure is a deterministic compile-time/manifest condition, not a runtime-dependent one. It is rated High (rather than Critical) because exploitation requires local physical/USB access rather than a remote vector, and credentials that are encrypted at rest are only partially mitigated (the in-process/`run-as` threat remains).

### Detection

The rule fires when an Android APK is both:

1. debuggable — the merged manifest declares `android:debuggable="true"` on the `<application>` element (or the attribute is explicitly set to `true`); and
2. ships Flipper instrumentation — the DEX bytecode contains Flipper classes such as `com/facebook/flipper/` (e.g. `FlipperOkhttpInterceptor`, `NetworkFlipperPlugin`, `DatabasesFlipperPlugin`, `SharedPreferencesFlipperPlugin`).

```xml
<application android:debuggable="true">
```
