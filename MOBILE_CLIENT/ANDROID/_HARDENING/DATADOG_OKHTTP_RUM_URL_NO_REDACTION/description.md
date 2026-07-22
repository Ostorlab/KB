The Datadog Android RUM SDK ships an OkHttp integration (`dd-sdk-android-okhttp`) composed of a `DatadogInterceptor` (an application interceptor) and a `DatadogEventListener.Factory()`. When both are registered on a shared `OkHttpClient`, every request the client makes is recorded as a RUM **resource** whose `resource.url` is the full request URL — host, path **and query string** — with no redaction applied by default.

The vulnerability arises when this instrumentation is registered **without configuring a resource URL mapper** that strips or obfuscates query parameters before the resource event is serialized and uploaded to Datadog. With no mapper, the SDK records the raw URL verbatim, so any value placed in a request's query string is shipped to the Datadog RUM backend and attributed to the current user (when `Datadog.setUserInfo` / `setUserId` is set).

This is a **defense-in-depth / hardening gap** rather than an active high-impact exposure. Today's impact is bounded by what callers actually put in query strings:

* If the only OkHttp query parameters are low-sensitivity app metadata (for example `app_name`, `os`, `app_version` on a heartbeat endpoint), the captured URLs expose only endpoint paths and app version — normal RUM telemetry.
* The gap becomes a real data-exfiltration concern the moment a `GET` request places an identifier or PHI (`userId`, `appointmentId`, `messageThreadId`, `accountNumber`, token-like values, etc.) in the query string. A generic `buildGetRequest(path, queryParams)` helper that appends arbitrary caller-supplied parameters and routes them through the same instrumented client turns any such future caller into an un-redacted leak to Datadog RUM.

Note that this OkHttp vector does **not**, by default, capture:

* The `Authorization` bearer token — provided the `DatadogInterceptor` is ordered *before* the interceptor that attaches the `Authorization` header, and the SDK's first-party header-capture overload (`Map<host, Set<headerName>>`) is **not** used.
* Request bodies (REST payloads, GraphQL `operationName`/`variables`) or response bodies — the SDK records resource size, status, timing and OkHttp error text only.

WebView traffic loaded via `WebView.loadUrl(...)` uses Chromium's network stack, not the app's `OkHttpClient`, so it is out of scope for this vector (a separate WebView disclosure concern).

### Example (vulnerable configuration)

=== "Kotlin"
  ```kotlin
  import com.datadog.android.core.sampling.RateBasedSampler
  import com.datadog.android.okhttp.DatadogEventListener
  import com.datadog.android.okhttp.DatadogInterceptor
  import okhttp3.OkHttpClient

  // No BuildConfig.DEBUG gate; no resource URL mapper configured.
  val client: OkHttpClient = OkHttpClient.Builder()
      .addInterceptor(
          DatadogInterceptor.Builder(listOf(apiUrl))
              .setTraceSampler(RateBasedSampler(100f))
              .build()
      )
      .eventListenerFactory(DatadogEventListener.Factory())
      .build()
  ```
