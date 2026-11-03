Android `WebView` components delegate TLS server-certificate validation to
the platform. When the embedded browser engine encounters a certificate it
cannot validate (for example an expired, self-signed, or hostname-mismatched
certificate), it notifies the attached `WebViewClient` through the
[`onReceivedSslError(WebView, SslErrorHandler, SslError)`](https://developer.android.com/reference/android/webkit/WebViewClient#onReceivedSslError(android.webkit.WebView,%20android.webkit.SslErrorHandler,%20android.net.http.SslError))
callback and **cancels the connection by default**. The application decides
what happens next through the `SslErrorHandler`: calling
[`cancel()`](https://developer.android.com/reference/android/webkit/SslErrorHandler#cancel%28%29)
keeps the platform default (abort the request), while calling
[`proceed()`](https://developer.android.com/reference/android/webkit/SslErrorHandler#proceed%28%29)
**loads the page despite the invalid certificate**.

A `WebViewClient` implementation that overrides `onReceivedSslError` and
calls `handler.proceed()` without performing full certificate validation
disables TLS server authentication for the WebView. An attacker positioned
on the network (rogue access point, ARP spoofing, hostile proxy, compromised
router) can present **any** invalid certificate — self-signed, expired, or
issued for another name — and the app will render the attacker's content as
if it were legitimate. All traffic carried by that WebView session, including
session cookies, bearer tokens, credentials typed into forms, and any
JavaScript bridges exposed to the page, is then readable and modifiable by
the attacker. Because the WebView UI is the app's own UI, users get no
browser warning they could act on.

This is a specialization of [CWE-295 (Improper Certificate
Validation)](https://cwe.mitre.org/data/definitions/295.html) and of the
OWASP MASVS-NETWORK requirement that mobile apps perform proper certificate
validation ([MASWE-0027: Insecure Certificate
Validation](https://mas.owasp.org/MASWE/MASVS-NETWORK/MASWE-0027/)). The
Android reference documentation states it explicitly: *"If this method is
overridden, it is up to the developer to properly handle the SSL error"* and
apps should respond by cancelling the request; the platform guidance
discourages calling `proceed()` in response to an SSL error, and also
discourages prompting the user, since users cannot meaningfully evaluate
certificate errors.

### Vulnerable patterns

The following patterns are all considered vulnerable per
[MASTG-TEST-0284: Incorrect SSL Error Handling in
WebViews](https://mas.owasp.org/MASTG/tests/android/MASVS-NETWORK/MASTG-TEST-0284/):

1. **Unconditionally accepting SSL errors** — calling `handler.proceed()`
   without checking the nature of the error:

=== "Java"
    ```java
    public class InsecureWebViewClient extends WebViewClient {
        @Override
        public void onReceivedSslError(WebView view, SslErrorHandler handler, SslError error) {
            // Ignores every certificate error: self-signed, expired, wrong hostname...
            handler.proceed();
        }
    }
    ```

=== "Kotlin"
    ```kotlin
    webView.webViewClient = object : WebViewClient() {
        override fun onReceivedSslError(view: WebView, handler: SslErrorHandler, error: SslError) {
            handler.proceed()
        }
    }
    ```

2. **Relying only on the primary error code** — using
   [`SslError.getPrimaryError()`](https://developer.android.com/reference/android/net/http/SslError#getPrimaryError%28%29)
   for the proceed decision, such as proceeding whenever the primary error is
   not `SSL_UNTRUSTED`. The primary error is only the first of the errors
   found in the certificate chain; a certificate can still be invalid for the
   host (or carry additional chain errors) while the primary code looks
   benign. Any decision path that ends in `proceed()` bypasses validation:

=== "Java"
    ```java
    @Override
    public void onReceivedSslError(WebView view, final SslErrorHandler handler, SslError error) {
        if (error.getPrimaryError() == SslError.SSL_IDMISMATCH) {
            // Still bypasses TLS: hostname-mismatched certificates are accepted.
            handler.proceed();
        } else {
            super.onReceivedSslError(view, handler, error);
        }
    }
    ```

3. **Silently suppressed failures** — catching exceptions inside the handler
   (or swallowing the error path) without calling `cancel()`, which can let
   the connection continue instead of failing closed.

### Benign look-alikes

Not every `onReceivedSslError` override is vulnerable, and a detector must
distinguish the cases:

* **Correct implementation** — the override calls `handler.cancel()` (or
  `super.onReceivedSslError(...)`, whose platform default is to cancel).
  This is the recommended behavior.

=== "Java"
    ```java
    public class SafeWebViewClient extends WebViewClient {
        @Override
        public void onReceivedSslError(WebView view, SslErrorHandler handler, SslError error) {
            // Fail closed, keep the platform protection.
            handler.cancel();
        }
    }
    ```

* **Empty override** — an override with an empty body neither proceeds nor
  cancels; it does not accept the invalid certificate (the request hangs
  instead). It is a code-quality smell rather than a certificate-validation
  bypass.
* **Debug-gated proceed** — several hybrid frameworks (notably Apache
  Cordova's `SystemWebViewClient`) accept SSL errors only while the app
  build is debuggable and cancel otherwise. In a non-debuggable release
  build the `proceed()` branch is unreachable, so the shipped artifact is
  not vulnerable to this weakness (the debuggability of the build is
  reported separately).

The vulnerability requires: a `WebViewClient` subclass (named, anonymous, or
transitively inherited) that overrides `onReceivedSslError`, a reachable call
to `SslErrorHandler.proceed()` in that override that is not gated behind a
debug-only flag, and the WebView actually being used to load remote content
over HTTPS. The impact is a full machine-in-the-middle position over the
WebView session: credential theft, session hijacking, content injection, and
— when JavaScript bridges or file access are enabled for the WebView —
potential escalation into the app's native attack surface.
