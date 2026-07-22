- Disable debug mode on every build type intended for distribution: set `isDebuggable = false` on all non-internal build types (`prod`, `staging`, `dev`, `pentest`, `release`). Only the local `debug` build type should remain debuggable, and debuggable builds must never be shipped to end users.
- Optionally set `android:debuggable="false"` explicitly on the `<application>` tag in `AndroidManifest.xml` as defense in depth, since when the attribute is absent the effective flag is governed solely by the Gradle build type.
- Encrypt sensitive data at rest so that even if a private file is recovered it cannot be read. For SQLite caches, use an encrypted variant (for example SQLCipher / `SupportFactory`, or the Apollo `apollo-normalized-cache-sqlcipher` variant) with a key derived from the Android Keystore, and avoid persisting secrets such as passcodes in the normalized cache.
- Enforce the configuration in CI: add a Gradle check task that fails the build if any build type other than `debug` leaves `isDebuggable` unset or set to `true`.
- Verify the fix by rebuilding each build type and confirming the generated APK's `AndroidManifest.xml` contains `android:debuggable="false"` (inspect with `aapt dump xmltree app.apk AndroidManifest.xml`), and by confirming that `adb shell run-as <package>` is refused (`package not debuggable`) on the hardened builds.

=== "Kotlin"

  ```kotlin
  buildTypes {
      getByName("release") {
          isMinifyEnabled = true
          isDebuggable = false
          signingConfig = signingConfigs.getByName("release")
      }
      create("prod") {
          isMinifyEnabled = true
          isDebuggable = false
          signingConfig = signingConfigs.getByName("release")
          applicationIdSuffix = ".production"
      }
      create("staging") {
          isMinifyEnabled = false
          isDebuggable = false
          signingConfig = signingConfigs.getByName("release")
          applicationIdSuffix = ".staging"
      }
      create("dev") {
          isMinifyEnabled = false
          isDebuggable = false
          signingConfig = signingConfigs.getByName("release")
          applicationIdSuffix = ".dev"
      }
      getByName("debug") {
          // Only the local debug build type remains debuggable.
          isMinifyEnabled = false
          signingConfig = signingConfigs.getByName("debug")
          applicationIdSuffix = ".debug"
      }
  }
  ```
