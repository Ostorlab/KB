# Sensitive data retained in image cache after logout

The application caches server-controlled content (for example images rendered by an image-loading library such as Coil, Glide or Picasso, or resources fetched by a `WebView`) to the application-private disk cache directory. When the user logs out, the application clears its primary session stores — such as the GraphQL/Apollo normalized cache (memory and SQLite), the OAuth token and the application settings — but does **not** clear the image or `WebView` disk cache.

As a result, potentially sensitive content fetched from authenticated endpoints — including health (PHI) article or survey imagery — persists in the OS-sandboxed application private cache directory after the session ends and remains recoverable until the cache is evicted or the application data is cleared.

Real-world impact is limited because the cache lives in the application sandboxed private directory and extraction requires root or physical access to the device. This is therefore an informational data-retention note rather than an exploitable vulnerability, but it is still relevant on shared, lost or rooted devices and for compliance with data-minimisation and data-retention requirements.
