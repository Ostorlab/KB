Never call `SslErrorHandler.proceed()` in response to an SSL error. The
platform default is safe: when `onReceivedSslError` is **not** overridden,
the `WebView` cancels the request. If the callback must be overridden (for
example to log or annotate TLS failures), the implementation must fail
closed by calling `handler.cancel()`, or by delegating to
`super.onReceivedSslError(view, handler, error)`.

=== "Java"
    ```java
    public class SecureWebViewClient extends WebViewClient {
        @Override
        public void onReceivedSslError(WebView view, SslErrorHandler handler, SslError error) {
            // Fail closed: never load content behind an invalid certificate.
            handler.cancel();
        }
    }
    ```

=== "Kotlin"
    ```kotlin
    webView.webViewClient = object : WebViewClient() {
        override fun onReceivedSslError(view: WebView, handler: SslErrorHandler, error: SslError) {
            handler.cancel()
        }
    }
    ```

Additional guidance:

* **Do not prompt the user.** Android's security guidance discourages asking
  users whether to proceed past a certificate error: users cannot evaluate
  certificate validity, and the dialog trains them to accept warnings.
* **Do not "whitelist" error codes.** Decisions built on
  `SslError.getPrimaryError()` (for example "proceed unless
  `SSL_UNTRUSTED`") still accept invalid certificates and remain
  vulnerable. There is no safe subset of certificate errors to ignore.
* **Remove debug-gated `proceed()` branches from release artifacts.**
  Framework code such as Apache Cordova's `SystemWebViewClient` accepts SSL
  errors only in debuggable builds; ensure release builds are produced with
  `android:debuggable="false"` (the default for release builds) and strip or
  gate the branch behind `BuildConfig.DEBUG` verification that cannot be
  enabled at runtime.
* **If the WebView must talk to a server whose certificate cannot be
  validated by the platform** (for example a self-signed internal endpoint),
  use the [Android network security
  configuration](https://developer.android.com/training/articles/security-config)
  to trust a specific CA or to pin the server's certificate set. This keeps
  validation explicit, reviewable, and narrow instead of disabling it
  process-wide for the WebView.
* **Layered defenses**: keep `WebView` JavaScript and file access disabled
  unless needed, restrict `setJavaScriptEnabled`/`addJavascriptInterface`
  surfaces, and consider certificate pinning for the most sensitive
  endpoints so that a single missed validation path does not expose the whole
  session.
