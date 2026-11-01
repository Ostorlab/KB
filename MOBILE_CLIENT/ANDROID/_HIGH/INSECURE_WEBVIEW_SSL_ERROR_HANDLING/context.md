The "Insecure WebView SSL error handling" weakness disables TLS server
authentication for a mobile app's embedded browser component. It has
well-documented real-world consequences:

### Real-World Examples
- A large-scale study of 1,000 popular free Android apps (Fahl et al., *"Why
  Eve and Mallory Love Android: SSL Certificate Validation in Android Apps"*, ACM CCS 2012)
  found that a substantial share of apps did not validate certificates
  properly, including apps whose `WebViewClient` implementations accepted any
  invalid certificate in `onReceivedSslError`, leaving their users open to
  machine-in-the-middle attacks on hostile networks
  ([paper](https://dl.acm.org/doi/10.1145/2382196.2382205)).
- Google Play's App Security Improvement program explicitly warns
  developers shipping apps that override `onReceivedSslError` with
  `SslErrorHandler.proceed()`, treating it as a security defect that must be
  fixed before distribution. The WebView SSL error handler pattern is one of
  the long-standing automated warnings raised to developers in Play Console.
- The pattern repeatedly surfaces in security reviews of hybrid apps: Apache
  Cordova itself shipped a debug-gated `proceed()` inside
  `SystemWebViewClient`, which analysis tools have flagged in thousands of
  Cordova-based apps even though the branch is only reachable in debuggable
  builds — illustrating why detection must consider build debuggability
  rather than the mere presence of a `proceed()` call.

### Business Impact
- **Credential and session theft**: an attacker on the same network can
  capture login forms, cookies and bearer tokens rendered inside the
  compromised WebView, leading to account takeover.
- **Content and transaction manipulation**: injected content can alter
  displayed payee names, amounts or instructions inside what users believe is
  a trusted in-app page, enabling fraud that is indistinguishable from
  legitimate UI.
- **Compliance exposure**: unvalidated server certificates conflict with
  PCI DSS, SOC 2 and GDPR expectations for protecting data in transit over
  public networks, and complicate incident response after a suspected
  interception.
- **Regulatory and reputational fallout**: apps that ship this weakness are
  flagged by store security programs and mobile application security
  assessments (OWASP MASVS / MASTG-based reviews list it under
  MASVS-NETWORK), which can block releases and erode customer trust.

These cases and impacts underscore that accepting invalid certificates
inside a `WebView` is equivalent to removing TLS for the affected session,
and must be treated as a high-severity transport-security defect rather than
a cosmetic code smell.
