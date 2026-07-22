Validate image URLs before handing them to image loading libraries. Restrict the scheme to `https` (and a documented allowlist of hosts), reject `javascript:`, `data:` and `file:` schemes, and block RFC1918, loopback and link-local ranges (including `169.254.169.254`). Centralize the validation so every image loading path applies it.

### Code Examples

#### Kotlin

```kotlin
private fun safeImageUrlOrNull(url: String?): String? {
    val u = url?.let { runCatching { android.net.Uri.parse(it) }.getOrNull() } ?: return null
    if (u.scheme !in listOf("https", "http")) return null // drop javascript:/data:/file:
    if (isPrivateOrLoopback(u.host)) return null            // block 10/8, 172.16/12, 192.168/16, 127/8, 169.254/16
    if (u.host !in ALLOWED_IMAGE_HOSTS) return null         // host allowlist
    return u.toString()
}

// ImageRequest.Builder(...).data(safeImageUrlOrNull(imageUrl))
```
