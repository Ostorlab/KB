Detect rooted/jailbroken devices at runtime and refuse to run — or restrict sensitive functionality — when indicators are found. Combine several signals; any single check is trivial to bypass.

=== "Kotlin"
	```kotlin
	import android.content.Context
	import android.content.pm.PackageManager
	import android.os.Build
	import java.io.File

	fun isDeviceRooted(context: Context): Boolean {
	    // 1. Common su binary locations.
	    val suPaths = arrayOf(
	        "/system/bin/su", "/system/xbin/su", "/sbin/su",
	        "/system/app/Superuser.apk", "/system/etc/init.d/99SuperSUDaemon"
	    )
	    if (suPaths.any { File(it).exists() }) return true

	    // 2. Build tags set to test-keys on custom/rooted ROMs.
	    if (Build.TAGS?.contains("test-keys") == true) return true

	    // 3. Known root-management packages.
	    val rootPackages = arrayOf(
	        "com.topjohnwu.magisk",
	        "eu.chainfire.supersu",
	        "com.koushikdutta.superuser"
	    )
	    val pm = context.packageManager
	    for (pkg in rootPackages) {
	        try {
	            pm.getPackageInfo(pkg, 0)
	            return true
	        } catch (_: PackageManager.NameNotFoundException) {
	        }
	    }
	    return false
	}
	```

=== "Swift"
	```swift
	import Foundation
	import UIKit

	func isDeviceJailbroken() -> Bool {
	    #if targetEnvironment(simulator)
	    return false
	    #else
	    // 1. Common jailbreak file paths.
	    let suspiciousPaths = [
	        "/Applications/Cydia.app",
	        "/Applications/Sileo.app",
	        "/Library/MobileSubstrate/MobileSubstrate.dylib",
	        "/usr/sbin/sshd",
	        "/etc/apt",
	        "/private/var/lib/apt/",
	        "/var/jb"
	    ]
	    for path in suspiciousPaths where FileManager.default.fileExists(atPath: path) {
	        return true
	    }

	    // 2. Sandbox escape: writing outside the app container only succeeds on jailbroken devices.
	    let testPath = "/private/jb_probe.txt"
	    do {
	        try "x".write(toFile: testPath, atomically: true, encoding: .utf8)
	        try? FileManager.default.removeItem(atPath: testPath)
	        return true
	    } catch {
	        // Expected on a non-jailbroken device.
	    }

	    // 3. Suspicious URL schemes registered by jailbreak managers.
	    if let url = URL(string: "cydia://package/com.example.package"),
	       UIApplication.shared.canOpenURL(url) {
	        return true
	    }

	    return false
	    #endif
	}
	```

Additional hardening recommendations:

- Use the platform attestation service as the authoritative signal, validated server-side: **Play Integrity API** (`MEETS_DEVICE_INTEGRITY` / `MEETS_STRONG_INTEGRITY`) for Android, **DeviceCheck / App Attest** for iOS. Local checks are defense in depth, not the primary control.
- Perform the local checks in a native function (JNI on Android, plain C on iOS) and in multiple locations to resist patching and runtime hooking.
- Terminate or wipe sensitive state on detection — do not degrade gracefully, and do not surface a single, hookable "is rooted/jailbroken" boolean that an attacker can pin to `false`.
- Never gate critical security decisions on the client-side check alone; treat it as advisory on the client and authoritative only after a server-side attestation check.
