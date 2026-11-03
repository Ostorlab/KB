The rule reports a class implementing `javax.net.ssl.X509TrustManager` (directly or through `X509ExtendedTrustManager`) that defines a `checkServerTrusted` override whose body cannot reject a certificate:

- an empty body (the canonical "trust manager that does nothing"), or
- a body restricted to non-validating helpers such as logging or string building.

The report targets the class defining the unsafe override. When only a subclass is instantiated and it inherits the empty override without redefining it, the defining class is still reported: the inherited body is what runs for those instances.

Descendants that replace an unsafe `checkServerTrusted` signature are excluded from the report for the original body. This includes descendants inheriting a replacement from an intermediate class. If a descendant replaces only some `X509ExtendedTrustManager` overloads, such as the variants with `Socket` or `SSLEngine` parameters, the report covers only the unsafe overloads still inherited by instantiated descendants.

The coverage gap was in risk generation: before this rule, the static scanner had no detection for the weakness class, so an app shipping a trust-all manager was not reported at all.

**Suppressed shapes** (not reported, each covered by a regression fixture):

- the override throws (`throw`) or invokes any method outside the non-validating helper list — pinning managers and managers delegating to the platform default trust manager are skipped because the invoked code can reject;
- the trust manager class (and every subclass of it) is never instantiated in the app's DEX files — dead code cannot validate any connection;
- every allocation is unreachable on release control-flow paths after evaluating a recognized `BuildConfig.DEBUG` or `ApplicationInfo.flags & FLAG_DEBUGGABLE` branch, and the shipped build is not debuggable. Unrelated debug reads, other flag bits, inverted guards and allocations after a branch rejoins do not suppress a finding. Unknown branch patterns retain both paths. A debug-gated trust manager in a debuggable build is reported, since the branch stays reachable.

**Known open gaps** (documented rather than covered, to keep false positives low):

- a body that only calls `X509Certificate.checkValidity()` is not reported: it validates expiry only (MASTG-TEST-0282 lists it as a failure), but the invoked API can throw, so the rule cannot distinguish it from a validating body without deeper analysis;
- a body that catches and suppresses the `CertificateException` of a delegating call is not reported: detecting the swallowed exception requires try/catch analysis of the DEX bytecode;
- certificate-getter logging bodies are not reported: getters such as `getSubjectDN()`, `getIssuerDN()`, and `getPublicKey()` are outside the helper allowlist. Any future expansion must use exact method targets and account for getters such as `getEncoded()` that can throw;
- trust managers used only through reflection are not reported.

Detection is static, at the DEX bytecode level, mirroring OWASP MASTG-TEST-0282. The MASTG demo rule that flags every `checkServerTrusted` override is deliberately not reproduced as-is: it cannot distinguish a trust-all body from a validating one, which is exactly the review burden this rule removes.
