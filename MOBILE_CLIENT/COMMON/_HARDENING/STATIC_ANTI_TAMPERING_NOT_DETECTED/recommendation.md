# Static Anti-Tampering Hardening (Open-Source)

To mitigate the absence of static anti-tampering protections, mobile applications should implement a **defense-in-depth strategy at build time**, combining **open-source obfuscation, integrity enforcement mechanisms, and secure build practices**.

---

## 1. Advanced Code Obfuscation & Transformation

Obfuscation should go beyond renaming and include **control-flow obfuscation, string encryption, and class repackaging** using open-source tooling.

### Android (R8 / ProGuard)

R8 (default in Android builds) should be configured aggressively.

#### Configuration (`build.gradle`)
```groovy
android {
    buildTypes {
        release {
            minifyEnabled true
            shrinkResources true
            debuggable false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
}
```

#### Advanced Rules (`proguard-rules.pro`)
```proguard
# Keep entry points
-keep public class * extends android.app.Activity
-keep public class * extends android.app.Application

# Keep models used in serialization
-keep class com.yourapp.models.** { *; }

# Aggressive obfuscation
-repackageclasses 'a.b'
-flattenpackagehierarchy
-allowaccessmodification
-overloadaggressively
-useuniqueclassmembernames

# Remove logs
-assumenosideeffects class android.util.Log {
    public static *** d(...);
    public static *** v(...);
    public static *** i(...);
}
```

---

### iOS (Swift / Objective-C Obfuscation)

iOS lacks built-in obfuscation, but open-source tools can be integrated.

#### Open-Source Tools
- SwiftShield (symbol obfuscation)
- llvm-obfuscator (Obfuscator-LLVM for control-flow obfuscation)
- strip / dsymutil (symbol stripping)

#### Example: SwiftShield Integration
```bash
brew install swiftshield

swiftshield obfuscate \
  -p YourApp.xcodeproj \
  -t YourTarget \
  -s Sources/
```

#### Xcode Build Phase Script
```bash
if [ "$CONFIGURATION" = "Release" ]; then
    swiftshield obfuscate -p "$PROJECT_FILE_PATH" -t "$TARGET_NAME"
fi
```

---

## 2. Runtime Signature Verification (Static Integrity Anchor)

Ensures the application has not been **re-signed or tampered with**.

### Android (Kotlin)
```kotlin
fun verifySignature(context: Context): Boolean {
    val expectedHash = "YOUR_BASE64_SHA256_HASH"

    return try {
        val packageInfo = context.packageManager.getPackageInfo(
            context.packageName,
            PackageManager.GET_SIGNING_CERTIFICATES
        )

        val signatures = packageInfo.signingInfo.apkContentsSigners

        signatures.any { signature ->
            val digest = MessageDigest.getInstance("SHA-256")
                .digest(signature.toByteArray())

            val currentHash = Base64.encodeToString(digest, Base64.NO_WRAP)
            currentHash == expectedHash
        }
    } catch (e: Exception) {
        false
    }
}
```

---

### iOS (Swift)
```swift
func verifyAppIntegrity() -> Bool {
    guard let path = Bundle.main.executablePath,
          let data = try? Data(contentsOf: URL(fileURLWithPath: path)) else {
        return false
    }

    let hash = SHA256.hash(data: data)
    let computed = Data(hash).base64EncodedString()

    return computed == "EXPECTED_HASH"
}
```

---

## 3. Open-Source Packing & Binary Hardening Techniques

While fully featured packers are mostly commercial, several **open-source techniques** can approximate packing and hardening.

### Android

#### Techniques
- APK repacking with zipalign + apksigner
- DEX encryption (custom loader approach)
- Native library protection via NDK (move sensitive logic to C/C++)
- String encryption via custom utilities

#### Example: Basic String Encryption (Kotlin)
```kotlin
object StringObfuscator {
    fun xor(input: String, key: Char): String {
        return input.map { it.code.xor(key.code).toChar() }.joinToString("")
    }
}
```

---

### iOS

#### Techniques
- LLVM-based obfuscation (Obfuscator-LLVM)
- Binary stripping
- Splitting sensitive logic into dynamic libraries
- Manual function inlining / control-flow flattening

#### Example: Strip Symbols
```bash
strip -S -x YourAppBinary
```

---

## 4. Static Resource & Asset Protection

Sensitive assets should never remain in plaintext inside the package.

### Android (Encrypt Assets)
```kotlin
fun decryptAsset(context: Context, fileName: String, key: SecretKey): ByteArray {
    val encrypted = context.assets.open(fileName).readBytes()
    val cipher = Cipher.getInstance("AES")
    cipher.init(Cipher.DECRYPT_MODE, key)
    return cipher.doFinal(encrypted)
}
```

---

### iOS (Encrypt Files)
```swift
func decryptFile(data: Data, key: SymmetricKey) -> Data? {
    return try? AES.GCM.open(.init(combined: data), using: key)
}
```

---

## 5. Build Pipeline Hardening (CI/CD Integration)

Ensure protections are **systematically applied in release builds only**.

### Android (Gradle Enforcement)
```groovy
tasks.whenTaskAdded { task ->
    if (task.name.contains("Release")) {
        println("Applying security hardening...")
    }
}
```

---

### iOS (Xcode Conditional Build Setting)
```bash
if [ "$CONFIGURATION" != "Release" ]; then
    echo "Skipping protection for non-release build"
    exit 0
fi
```

---

## Key Takeaways

- Use **R8 / ProGuard with aggressive rules**
- Apply **open-source obfuscation tools (SwiftShield, Obfuscator-LLVM)**
- Implement **custom string and asset encryption**
- Enforce **signature and integrity verification**
- Harden binaries with **stripping, native code, and build-time transformations**
- Integrate protections into **CI/CD pipelines**

> No single control is sufficient—effective anti-tampering requires **layered protections applied statically at build time** using open and auditable tooling.