Imagine a healthcare or financial application that carefully protects its main screen with `FLAG_SECURE` so that screenshots and screen recordings of account balances, messages or a live video visit come out black. The same application also has a *second* `Activity` — a lock-screen incoming-call window that lights up the screen when a provider or caller rings, showing the caller's name and identifier right on the lock screen. Because `FLAG_SECURE` is a per-window flag and that second window never sets it, a co-resident application's `MediaProjection` session (started after the user taps "Start now" on the consent dialog), the device's stock screen recorder, or a screenshot taken while the incoming-call UI is visible captures the caller's name and identifier — sensitive, individually identifiable health or personal data — in plain text, on the very same production build that protects the main screen.

### Why it happens

* **`FLAG_SECURE` is per-Window, not per-app.** Setting it on one `Activity`'s window does not protect any other `Activity`'s window, even within the same process.
* **No shared base class.** When every `Activity` extends a framework class (such as `ComponentActivity`) directly, the flag cannot be inherited; each sensitive `Activity` must set it explicitly, and it is easy to forget a secondary window such as a lock-screen, notification-triggered or exported `Activity`.
* **Lock-screen windows are easy to miss.** Lock-screen `Activity` windows typically focus on `setShowWhenLocked(true)`, `setTurnScreenOn(true)` or `FLAG_KEEP_SCREEN_ON | FLAG_ALLOW_LOCK_WHILE_SCREEN_ON` to display over the keyguard, and `FLAG_SECURE` is simply never added to that code path.
* **Build guards hide one variant.** Gating the flag on `if (!BuildConfig.DEBUG)` leaves at least the `debug` build variant unprotected and signals that screen capture is intentionally allowed on some variant — a risky stance for any window that renders sensitive data.

### Real-world impact

* **PHI / PII exposure.** A lock-screen incoming-call UI that renders a provider/caller name and identifier exposes individually identifiable health information (the identity of a care provider and the fact that a care encounter is occurring), which is HIPAA-class data in a healthcare context.
* **No remote vector, but no attach required either.** Exploitation is not network-reachable and requires an external capture mechanism (the user's own recorder/screenshot, or a co-resident app's `MediaProjection` session after user consent) triggered while the sensitive window is on screen. On the non-debuggable production release build, capture succeeds with no debugger attach, frida or rooted device required.
* **Transient but real.** The sensitive window (for example an incoming-call lock-screen UI) is transient, which limits the capture window, but the exposed data is sensitive and the gap is present on every build variant including the shipped production build.

### Business impact

For organizations operating in healthcare, financial or other regulated sectors, the consequences can include regulatory exposure (HIPAA / GDPR / CCPA), reputational damage from a privacy incident, and loss of user trust. Applying `FLAG_SECURE` unconditionally to every sensitive-data window is a low-cost, high-value hardening control.
