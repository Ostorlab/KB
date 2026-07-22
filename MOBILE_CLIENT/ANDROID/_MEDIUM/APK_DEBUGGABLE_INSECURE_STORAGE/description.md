The `android:debuggable` flag (or the Gradle `isDebuggable` build type property) determines whether an Android application can be debugged. When a production-oriented build type such as `prod`, `staging` or `dev` is shipped with `isDebuggable = true` (or the default `debug` build type is distributed), `adb shell run-as <package>` executes as the application UID and can read the application's private directory, including `/data/data/<package>/databases/*` and `/data/data/<package>/shared_prefs/*`.

This exposes any cleartext sensitive data the application persists in its private storage — plaintext SQLite caches (for example Apollo, Room or raw `SQLiteOpenHelper` databases), shared preferences, and cached authentication credentials — to extraction without device root. Setting `android:allowBackup="false"` blocks the standard `adb backup` vector but does **not** block `run-as` on a debuggable build, because `run-as` runs as the application UID and reads the private directory directly.

The realistic impact is non-root recovery of regulated data (PHI/PII) and stored credentials from a debuggable build installed on a physically accessible device with USB debugging enabled. The risk is rated Medium because the impact (sensitive data disclosure) is serious but gated behind physical access, USB debugging being enabled, and a debuggable build being distributed.

The following Gradle configuration ships debuggable production build types:

```kotlin
buildTypes {
    getByName("release") {
        isMinifyEnabled = true
        isDebuggable = false            // hardened
        signingConfig = signingConfigs.getByName("release")
    }
    create("prod") {
        isMinifyEnabled = false
        isDebuggable = true             // debuggable — run-as reachable
        signingConfig = signingConfigs.getByName("debug")
        applicationIdSuffix = ".production"
    }
    create("staging") {
        isMinifyEnabled = false
        isDebuggable = true             // debuggable
        signingConfig = signingConfigs.getByName("debug")
        applicationIdSuffix = ".staging"
    }
    create("dev") {
        isMinifyEnabled = false
        isDebuggable = true             // debuggable
        signingConfig = signingConfigs.getByName("debug")
        applicationIdSuffix = ".dev"
    }
    getByName("debug") {
        // isDebuggable defaults to true
    }
}
```

With a debuggable build installed and USB debugging enabled, an attacker with physical access and **no device root** can extract the private database:

```bash
$ adb shell run-as com.example.app cat /data/data/com.example.app/databases/app.db > /sdcard/app.db
$ adb pull /sdcard/app.db
$ sqlite3 app.db .dump
```
