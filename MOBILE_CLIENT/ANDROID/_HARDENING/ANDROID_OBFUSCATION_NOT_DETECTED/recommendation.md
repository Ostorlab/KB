Enable obfuscation in Android release builds so the shipped application is harder to reverse engineer and modify.

The default open-source Android option is **R8**, which is built into the Android build toolchain.

```groovy
android {
    buildTypes {
        debug {
            minifyEnabled false
        }
        release {
            minifyEnabled true
            shrinkResources true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
}
```

Start with conservative keep rules and expand only when runtime behavior breaks:

```proguard
-keep class * extends android.app.Activity
-keep class * extends android.app.Application
-keepclassmembers class * implements android.os.Parcelable {
    public static final android.os.Parcelable$Creator *;
}
-keepattributes *Annotation*
```

Available open-source Android options:

- **R8**: Default Android code shrinker and obfuscator for Java and Kotlin bytecode.
- **ProGuard**: Legacy open-source shrinker and obfuscator still used in some Android builds and rule sets.
- **jadx**: Useful to review the released Android package and confirm class names, methods, and logic are no longer trivially readable after obfuscation.
- **APKTool**: Useful to inspect the final Android package structure, manifest, and resources and verify what is still easily exposed.
- **Obfuscator-LLVM**: Can be used for Android native code when sensitive logic is implemented in C or C++ via the NDK.

Additional hardening recommendations:

- Run obfuscation only for release builds and enforce it in CI.
- Decompile the final release artifact with `jadx` and inspect resources with `apktool` to verify the protection is actually present.
- Do not rely on obfuscation alone for secrets, trust decisions, or license checks; validate those server-side as well.
- Re-test obfuscation coverage after major refactors or when adding new modules.
