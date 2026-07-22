To mitigate the risk associated with CVE-2023-3635, consider the steps below:

1. Upgrade the OkHttp dependency to a fixed version (`>= 4.12.0`) in the build configuration (for example
   `buildSrc/.../buildsrc/Versions.kt`: `const val okhttp = "4.12.0"` or newer), then re-run Gradle dependency
   resolution to confirm `com.squareup.okhttp3:okhttp` resolves to the patched version across all modules.
2. Pin OkHttp to the latest stable release and add a regression test or a Dependabot/Renovate rule to alert on
   vulnerable OkHttp versions.
3. As defense-in-depth for response-body sinks, validate the `Content-Encoding` header and add a max-size guard before
   streaming a body (for example in a download worker), to bound decompression work if a future gzip bug appears.
4. Keep cleartext traffic disabled (no `usesCleartextTraffic`, no cleartext `ConnectionSpec`) so a future MitM cannot
   inject crafted gzip bodies without a TLS/certificate compromise.
