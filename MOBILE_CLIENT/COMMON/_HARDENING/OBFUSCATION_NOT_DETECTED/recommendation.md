Implement obfuscation in release builds so the shipped application is harder to reverse engineer and modify.

=== "Android"
    Use the Android build pipeline to obfuscate Java or Kotlin code in production builds. The default open-source option is **R8**, which is built into the Android toolchain.

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
    - **APKTool**: Useful to verify whether the final APK still exposes readable resources, manifest details, or easy-to-modify structure.
    - **jadx**: Useful to review the released APK and confirm class names, methods, and logic are no longer trivially readable after obfuscation.
    - **Obfuscator-LLVM**: Can be used for Android native code when sensitive logic is implemented in C or C++ via the NDK.

    Practical Android recommendations:

    - Run obfuscation only for release builds and enforce it in CI.
    - Decompile the final release APK or AAB with `jadx` and inspect resources with `apktool` to verify the protection is actually present.
    - Move highly sensitive logic to native code only when justified, and protect it separately; native code is harder to analyze, but not impossible to reverse engineer.
    - Do not rely on obfuscation alone for API secrets, trust decisions, or license checks; validate those server-side as well.

=== "iOS"
    iOS does not provide an equivalent built-in obfuscation pipeline for Swift or Objective-C code, so teams usually combine symbol stripping, release-build hygiene, and selective obfuscation of sensitive code paths.

    Available open-source iOS options:

    - **SwiftShield**: Renames Swift symbols to make reverse engineering more difficult.
    - **Obfuscator-LLVM**: Can be applied to native code paths compiled through LLVM, especially for sensitive C or C++ components.
    - **strip**: Removes symbol information from production binaries.

    Practical iOS recommendations:

    - Strip symbols from release binaries and ensure verbose debug metadata is not shipped in production IPAs.
    - Review the final app binary with common reversing tools to confirm meaningful symbol names and implementation clues are reduced.
    - Keep sensitive enforcement logic layered with anti-tampering and backend-side verification instead of relying on obfuscation by itself.

Additional hardening recommendations:

- Re-test obfuscation coverage after major refactors or when adding new modules.
- Avoid embedding long-lived secrets, private keys, or irreversible trust logic directly in client code.
- Treat obfuscation as one resilience layer alongside anti-tampering, anti-debugging, and strong server-side controls.
