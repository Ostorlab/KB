Never ship a debuggable build that also packages Flipper instrumentation to any real user or environment.

1. Make production-class build types non-debuggable. In `build.gradle.kts`, set `isDebuggable = false` for every build type that can reach real users (production, staging, etc.), and resolve library module variants to their `release` variant via `matchingFallbacks += listOf("release")` so that any `if (BuildConfig.DEBUG)` gate that activates Flipper evaluates to `false`. Keep only the local `debug` build debuggable.

```kotlin
create("prod") {
    isMinifyEnabled = true
    isDebuggable = false
    matchingFallbacks += listOf("release")
}
```

2. Remove Flipper instrumentation from any distributable build. Strip `DatabasesFlipperPlugin`, `SharedPreferencesFlipperPlugin` and the Flipper network interceptor (`FlipperOkhttpInterceptor`) from every build that can reach users. Gate them behind a `debugImplementation`-only dependency or a dedicated internal build type so they are never packaged into a release/prod/staging APK.

3. Never attach a traffic-capturing interceptor to the authenticated `OkHttpClient` in a build that can be distributed. If debug traffic inspection is required, use a separate `OkHttpClient` that does not contain the `AuthorizationInterceptor`, or scope Flipper instrumentation to a non-production build type only.

4. Gate `FLAG_SECURE` on an explicit, non-debug flag (e.g. `BuildConfig.ENABLE_SCREENSHOTS`, defaulting to `false` and `true` only for the local debug build) instead of `!BuildConfig.DEBUG`, so screen-capture protection is applied in every build that can reach users regardless of debuggability.

```kotlin
if (!BuildConfig.ENABLE_SCREENSHOTS) {
    window.setFlags(
        WindowManager.LayoutParams.FLAG_SECURE,
        WindowManager.LayoutParams.FLAG_SECURE,
    )
}
```

5. Make the release signing configuration fail-fast when no real release keystore is configured, instead of silently falling back to the well-known debug keystore, so CI cannot silently ship a debug-key-signed "release" APK.
