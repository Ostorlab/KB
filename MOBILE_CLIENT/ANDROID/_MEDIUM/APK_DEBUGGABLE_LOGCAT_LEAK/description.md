A build type intended for distribution (for example a `prod` or `release` variant) is configured with `isDebuggable = true` (or otherwise resolves `BuildConfig.DEBUG` to `true`), and the application selects a logcat-writing logging tree — such as `Timber.DebugTree()` or direct `android.util.Log` calls — whenever that flag is set. As a result every diagnostic log statement that interpolates sensitive data is written to the Android `logcat` circular buffer on a distributable build.

Android `logcat` is readable by anyone with physical or USB access to the device through `adb logcat`, regardless of the Android version. On devices below Android 13 (API < 33), a co-installed malicious application holding the `READ_LOGS` permission can also read the system `logcat` output. Any sensitive value interpolated into a log statement — for example survey answers, health or biometric measurements, gender, contact identifiers, account or session identifiers — is therefore disclosed locally on the distributed build.

This is distinct from a genuinely debuggable `debug`/`dev`/`staging` build that is never distributed: the exposure arises only when a build type that carries a production-like identity (for example an `applicationIdSuffix = ".production"`) is shipped while still being debuggable, which routes the production logging sinks to `logcat` instead of to a non-logcat sink.

**Common attack scenarios:**

- **Local logcat capture:** An attacker with physical or USB access runs `adb logcat` on a distributed debuggable build and reads the sensitive values directly.
- **Co-installed malicious app:** On Android API 24-32, a malicious app holding `READ_LOGS` reads the same `logcat` output without physical access.
- **Debug-signed distribution:** A debuggable build type is often signed with the universal Android debug key and is non-minified, which makes the APK installable and inspectable on any sideload-enabled device and increases distribution realism.
