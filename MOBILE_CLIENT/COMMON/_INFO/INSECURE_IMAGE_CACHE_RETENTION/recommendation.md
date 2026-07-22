# Sensitive data retained in image cache after logout

Clear the image and `WebView` caches as part of the logout / session-termination flow so that no server-controlled content outlives the session.

## Coil (Android)

Clear the disk and memory caches when the user logs out:

```kotlin
fun logout(context: Context) {
    appSettings.clearStorage()
    encryptedPrefs.oauthToken = ""
    Api.apolloClient.apolloStore.clearAll()
    val loader = context.applicationContext.coilImageLoader()
    loader.diskCache?.clear()
    loader.memoryCache?.clear()
    // ...
}
```

For Coil3, implement a shared `SingletonImageLoader.Factory` so the loader can be cleared from a single place. Alternatively, disable the image disk cache for sensitive content via `.diskCachePolicy(CachePolicy.DISABLED)` on the relevant `ImageRequest`s.

## WebView (Android)

Call `WebView.clearCache(true)` and `WebView.clearHistory()` during logout, and consider `WebSettings.cacheMode = WebSettings.LOAD_NO_CACHE` for views that render authenticated content.

```kotlin
fun logout(context: Context) {
    // ...
    webView.clearCache(true)
    webView.clearHistory()
}
```

## iOS

Clear `URLCache.shared.removeAllCachedResponses()` and the disk cache of any image library (for example `SDImageCache.default().clearMemory()` and `SDImageCache.default().clearDisk()`, or `KingfisherManager.shared.cache.clearMemoryCache()` and `clearDiskCache()`) on logout.

```swift
func logout() {
    URLCache.shared.removeAllCachedResponses()
    SDImageCache.default().clearMemory()
    SDImageCache.default().clearDisk()
    // ...
}
```

## Verification

- After logout, inspect the application private cache directory and confirm no article/survey image files remain.
- Re-open the application unauthenticated and confirm no sensitive article/survey text or images are retrievable from cache.
