Enable obfuscation in Android release builds so the shipped application is harder to reverse engineer, analyze, and repackage.

For Android, the standard open-source approach is [**R8**](https://developer.android.com/studio/build/shrink-code), which is built into the Android Gradle toolchain.

### Native Android (Java / Kotlin)

Enable R8 in release builds:

```groovy
android {
    buildTypes {
        release {
            minifyEnabled true
            shrinkResources true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "r8-rules.pro"
            )
        }
    }
}
```

Create an `r8-rules.pro` file and keep only the code that must remain visible at runtime. A simple starting point is:

```text
-keep class * extends android.app.Activity
-keep class * extends android.app.Application
-keepclassmembers class * implements android.os.Parcelable {
    public static final android.os.Parcelable$Creator *;
}
-keepattributes *Annotation*
```

Extend the rules only where required for frameworks that depend on reflection, annotations, generated bindings, or serialization. Avoid broad keep rules for entire packages unless they are truly necessary, because they can significantly reduce the effectiveness of obfuscation.

### Flutter on Android

If the application is built with Flutter, enable Dart obfuscation for release builds. Flutter documents this in its [official obfuscation guide](https://docs.flutter.dev/deployment/obfuscate):

```bash
flutter build apk --release --obfuscate --split-debug-info=build/debug-info
flutter build appbundle --release --obfuscate --split-debug-info=build/debug-info
```

Keep the generated symbol files outside the distributed application. If the Flutter app includes Android platform code or native plugins, keep R8 enabled in the Android host application as well.

### React Native on Android

If the application uses React Native, enable **R8** in the Android release build for the native host application, bridge code, and embedded libraries. The same release-build example shown in the native Android section above can be used for the Android host application.

Also ensure production JavaScript bundles are created in release mode. If the project uses [Hermes](https://reactnative.dev/docs/Hermes), align the release build with production bundle settings and avoid shipping source maps or development artifacts with the distributed application.

### .NET MAUI on Android

If the application is built with .NET MAUI, follow the platform guidance for [trimming a .NET MAUI app](https://learn.microsoft.com/dotnet/maui/deployment/trimming). Release builds should enable Android code shrinking and managed-code trimming where compatible with the application architecture.

Where trimming or obfuscation affects reflection-heavy libraries, use targeted preservation rules instead of broadly disabling release hardening.

### Rollout approach

A phased rollout is usually the safest approach:

1. Enable obfuscation only for release builds.
2. Start with a minimal `r8-rules.pro` file and add keep rules only where runtime compatibility requires them.
3. Validate framework-specific behavior for serialization, reflection, dependency injection, and bridge code.
4. For Flutter, React Native, or .NET MAUI applications, confirm that platform-specific release artifacts and symbol files are handled correctly and that development artifacts are not distributed.
5. After major dependency or build-pipeline changes, review the release configuration again to ensure obfuscation is still applied effectively.

### Additional hardening recommendations

- Apply obfuscation only to release builds and keep debug artifacts, mapping files, and symbol files outside the distributed application.
- Review framework-specific keep rules carefully; excessive keep rules can effectively disable obfuscation.
- Avoid embedding long-lived secrets, trust decisions, or license checks directly in client code even when obfuscation is enabled.
- Use obfuscation alongside other hardening measures such as anti-tampering, anti-debugging, root detection, transport protections, and strong server-side authorization.
