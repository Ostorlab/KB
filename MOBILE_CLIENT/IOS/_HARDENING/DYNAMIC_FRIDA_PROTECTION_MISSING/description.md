The application remained functional while running under Frida-based dynamic instrumentation on iOS.

This indicates that the application does not detect, or does not meaningfully respond to, runtime instrumentation through Frida or Frida Gadget. An attacker who can instrument the application at runtime may observe internal state, alter control flow, intercept sensitive method calls, bypass local protections, and tamper with client-side security checks without modifying the IPA on disk.

On iOS, this is especially relevant for checks implemented only in the client, such as jailbreak heuristics, local anti-debug logic, feature gates, fraud signals, certificate-pinning helpers, or business rules enforced solely on-device. If Frida-based instrumentation is not detected, those controls can often be bypassed or observed dynamically.

This is a resilience weakness rather than a complete trust boundary failure: client-side anti-instrumentation can raise attacker cost, but sensitive authorization and trust decisions should still be enforced server-side.
