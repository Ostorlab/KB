# Static Anti-Tampering Hardening (Enterprise-Grade)

To mitigate the absence of static anti-tampering protections, mobile applications should implement a **defense-in-depth strategy at build time**, combining **advanced obfuscation, commercial-grade packers, and integrity enforcement mechanisms**.

---

## 1. Advanced Code Obfuscation & Transformation

Obfuscation should go beyond renaming and include **control-flow obfuscation, string encryption, and class repackaging**.

### Android (R8 / ProGuard + Hardening)

R8 is the baseline and should be configured aggressively.

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

iOS requires third-party tooling for real protection.

#### Enterprise Tools
- iXGuard (Guardsquare)
- Arxan (Digital.ai)
- Appdome
- SwiftShield (open-source baseline)

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

## 3. Commercial Packers & Application Protectors

These provide **binary encryption, anti-reversing, and anti-tampering protections** beyond standard obfuscation.

### Android (Enterprise Protectors)

#### Recommended Tools
- DexGuard (Guardsquare)
- Allatori
- SecNeo
- Tencent Jiagu

#### DexGuard Example
```groovy
buildTypes {
    release {
        minifyEnabled true
        proguardFiles getDefaultProguardFile('proguard-android.txt'),
                      'dexguard-project.txt'
    }
}
```

#### DexGuard Rules (`dexguard-project.txt`)
```proguard
# Enable string encryption
-encryptstrings class com.yourapp.**

# Class encryption
-encryptclasses class com.yourapp.secure.**

# Tamper detection
-checktamper

# Hide access
-obfuscatecode
```

---

### iOS (Enterprise Protectors)

#### Recommended Tools
- iXGuard (Guardsquare)
- Arxan (Digital.ai)
- Appdome

#### Example: iXGuard Configuration (Conceptual)
```bash
ixguard \
  --input YourApp.ipa \
  --output ProtectedApp.ipa \
  --obfuscate-control-flow \
  --encrypt-strings \
  --anti-tamper \
  --anti-debug
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

- Combine **R8 + enterprise packers** (DexGuard / iXGuard) for strong protection
- Apply **string, class, and control-flow obfuscation**
- Encrypt **sensitive assets and constants**
- Enforce **signature and integrity checks**
- Integrate protections into **CI/CD pipelines**

> No single control is sufficient—effective anti-tampering requires **layered protections applied statically at build time**.