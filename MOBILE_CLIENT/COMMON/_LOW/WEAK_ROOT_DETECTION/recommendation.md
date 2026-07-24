Make root/jailbreak detection robust, redundant, and re-verified across the app lifecycle so no single bypass defeats it.

- **Combine multiple independent indicators.** Do not rely on a single `su` PATH walk or a single stdout substring. AND-combine several signals: a `su`/`magisk` binary/file scan, `Build.TAGS` test-keys check, root-app package scan (e.g. `com.topjohnwu.magisk`, `eu.chainfire.supersu`), SELinux/mount-namespace introspection, and a SafetyNet/Play Integrity attestation request.
- **Use the process exit code, not stdout alone.** When spawning `su -c id`, call `waitFor()`/`exitValue()` and require both a `0` exit code **and** a `uid=0` line in the output. Read the full stream, not a single `readLine()`.
- **Do not swallow failures silently.** Log `exec` exceptions (e.g. via `Timber.w`) and treat repeated or patterned failures as suspicious rather than silently returning `false`.
- **Re-verify on resume.** Invoke the detector in `onResume()` (and optionally `onNewIntent`), not only in `onCreate`, so a single spawn-time hook does not defeat detection for the entire process lifetime.
- **Add compensating controls.** Add SafetyNet/Play Integrity attestation, signature self-verification, debugger/Xposed/Frida detection, and OkHttp `CertificatePinner` (TLS pinning) so that even if one detector is bypassed, other controls remain.

### Kotlin

```kotlin
object RootUtils {
    fun isDeviceRooted(): Boolean {
        if (!isRootAvailable()) return false
        var process: Process? = null
        return try {
            process = Runtime.getRuntime().exec(arrayOf("su", "-c", "id"))
            val output = process.inputStream.bufferedReader().readText()
            val exit = process.waitFor()
            output.lowercase().contains("uid=0") && exit == 0
        } catch (e: Exception) {
            Timber.w(e, "su exec failed")
            false
        } finally {
            process?.destroy()
        }
    }

    private fun isRootAvailable(): Boolean {
        val path = System.getenv("PATH") ?: return false
        return path.split(":").any { File(it, "su").exists() } ||
            Build.TAGS?.contains("test-keys") == true
    }
}
```

### Swift

```swift
func isJailbroken() -> Bool {
    let suspiciousPaths: [String] = [
        "/Applications/Cydia.app",
        "/Library/MobileSubstrate/MobileSubstrate.dylib",
        "/bin/bash", "/usr/sbin/sshd", "/etc/apt"
    ]
    if FileManager.default.fileExists(atPath: "/Applications/Sileo.app") { return true }
    for path in suspiciousPaths where FileManager.default.fileExists(atPath: path) {
        return true
    }
    return canOpen("cydia://package/com.example") || canOpen("sileo://package/com.example")
}
```
