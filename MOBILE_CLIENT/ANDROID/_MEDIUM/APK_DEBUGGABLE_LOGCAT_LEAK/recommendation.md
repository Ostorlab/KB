Ensure that every build type intended for distribution is non-debuggable so that a logcat-writing logging tree is never planted on a shipped build.

Set `isDebuggable = false` for the affected build type (or remove the build type and consolidate into the genuine non-debuggable `release` type), and sign it with the release configuration:

```kotlin
create("prod") {
    isMinifyEnabled = false
    isDebuggable = false
    signingConfig = signingConfigs.getByName("release")
    applicationIdSuffix = ".production"
    matchingFallbacks += listOf("release")
}
```

Gate the logging tree selection so that a logcat-writing tree is planted only for truly non-distributable build types, and route everything else to a non-logcat sink:

```kotlin
private fun initLogger() {
    if (BuildConfig.DEBUG && BuildConfig.BUILD_TYPE in listOf("debug", "dev", "staging")) {
        Timber.plant(Timber.DebugTree())
    } else {
        Timber.plant(ProductionLoggingTree())
    }
}
```

Additional recommendations:

- Remove sensitive fields from log statements entirely, or redact them before logging, so that PHI/PII never reaches any logging sink.
- Enforce `isDebuggable = false` and release signing for distribution build types through CI checks to prevent accidental release of debuggable builds.
- Verify the fix by building the affected variant, confirming `BuildConfig.DEBUG` resolves to `false`, and running `adb logcat` while triggering the sensitive flows to confirm no PHI/PII appears.
