CVE-2023-3635 is a denial-of-service vulnerability in OkHttp's `GzipSource`. A crafted GZIP sequence can cause
`GzipSource.read()` to return a negative byte count, which drives callers into an infinite loop or hang, resulting
in an availability-only impact (application freeze / denial of service).

OkHttp's internal `BridgeInterceptor` transparently wraps any HTTP response carrying `Content-Encoding: gzip` in
`GzipSource`. This behaviour is part of every `OkHttpClient`, including a bare `OkHttpClient.Builder().build()`, and
applies whether or not the application explicitly requests `Accept-Encoding: gzip`. The vulnerable `GzipSource` code
path is therefore reachable on every OkHttp client whenever a server returns a gzip-encoded response body that the
application then reads.

OkHttp versions before `4.12.0` are in the affected range. An application is exposed when it pins (or resolves)
`com.squareup.okhttp3:okhttp` to a version below `4.12.0` and consumes gzip-encoded response bodies (for example via
`ResponseBody.string()`, `byteStream()`, or a higher-level client such as Apollo that reads the body internally),
without an application-level interceptor that strips `Content-Encoding` / overrides the gzip bridge.

Runtime exploitability is constrained by who controls the response body: the DoS is only triggered if a server-trusted
endpoint the application fetches (its own backend, a CDN asset, or a remotely-influenced URL) can be made to return a
crafted GZIP sequence. With cleartext disabled and all response sources server-trusted, the residual risk is primarily
a dependency-hygiene / latent library weakness rather than a proven in-application DoS.
