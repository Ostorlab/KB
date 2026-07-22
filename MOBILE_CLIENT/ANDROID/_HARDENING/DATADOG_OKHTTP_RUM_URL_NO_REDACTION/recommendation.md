Configure URL redaction on the Datadog OkHttp instrumentation so query strings are never recorded in RUM resource URLs, and audit GET-request callers so identifiers/PHI never travel in query parameters.

### Redact the RUM resource URL

Use the SDK's resource event mapper to strip the query string, reducing every recorded resource URL to host + path. On current Datadog SDK releases, set `setResourceEventMapper` on the `RumConfiguration.Builder` and rewrite `resource.url`:

=== "Kotlin"
  ```kotlin
  val rumConfig = RumConfiguration.Builder(rumApplicationId)
      .setResourceEventMapper { resource ->
          // Keep host + path only; drop the query string from RUM.
          val stripped = resource.url.substringBefore("?")
          resource.copy(url = stripped)
      }
      .build()
  ```

On SDK 2.x where the mapper lives on the `DatadogInterceptor.Builder`, use `setResourceMapper`:

=== "Kotlin"
  ```kotlin
  val interceptor = DatadogInterceptor.Builder(listOf(apiUrl))
      .setTraceSampler(RateBasedSampler(100f))
      .setResourceMapper { resource ->
          val stripped = resource.url.substringBefore("?")
          resource.copy(url = stripped)
      }
      .build()
  ```

### Keep the bearer token out of scope

* Keep `DatadogInterceptor` ordered **before** the interceptor that attaches the `Authorization: Bearer <token>` header so the token is never observed by the Datadog interceptor.
* **Never** add `Authorization` to any first-party host header allow-list (do not switch to the `Map<host, Set<headerName>>` builder overload for the auth header).

### Keep local logging out of release

* Keep the Flipper network interceptor `BuildConfig.DEBUG`-gated (and its release source set a no-op).
* Do **not** introduce an `HttpLoggingInterceptor` with `Level.BODY` or `Level.HEADERS` in release builds.

### Audit GET-request callers

* Audit `buildGetRequest(path, queryParams)` callers and confirm no identifier/PHI values are ever placed in query parameters; route such values via path variables or POST bodies instead.
* After the change, re-grep the codebase for the resource mapper call and confirm a match, and verify via the Datadog RUM dashboard (or a local RUM capture) that resource URLs for query-bearing endpoints are recorded without their query strings.
