Verify at runtime that the app was installed by an authorized source and respond when it was not. Combine a local installer-package check (cheap, but spoofable) with a server-verified Play Integrity attestation (authoritative).

**Detection approaches:**

1. **Installer package verification:** Query which package installed the app and confirm it matches an allow-list of trusted installers (e.g. the Google Play Store, `com.android.vending`). On API 30+ use `getInstallSourceInfo`; fall back to `getInstallerPackageName` on older releases. A `null` installer indicates a sideloaded `adb install` or a direct APK install.

=== "Kotlin"
    ```kotlin
    private val TRUSTED_INSTALLERS = setOf(
        "com.android.vending",      // Google Play Store
        "com.google.android.feedback"
    )

    fun isFromTrustedInstaller(context: Context): Boolean {
        val pm = context.packageManager
        val installer = try {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
                pm.getInstallSourceInfo(context.packageName).installingPackageName
            } else {
                @Suppress("DEPRECATION")
                pm.getInstallerPackageName(context.packageName)
            }
        } catch (_: PackageManager.NameNotFoundException) {
            null
        }
        return installer in TRUSTED_INSTALLERS
    }
    ```

=== "Java"
    ```java
    private static final Set<String> TRUSTED_INSTALLERS = new HashSet<>(Arrays.asList(
        "com.android.vending", "com.google.android.feedback"
    ));

    public static boolean isFromTrustedInstaller(Context context) {
        PackageManager pm = context.getPackageManager();
        String installer = null;
        try {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
                installer = pm.getInstallSourceInfo(context.getPackageName())
                              .getInstallingPackageName();
            } else {
                installer = pm.getInstallerPackageName(context.getPackageName());
            }
        } catch (PackageManager.NameNotFoundException ignored) {
        }
        return installer != null && TRUSTED_INSTALLERS.contains(installer);
    }
    ```

2. **Play Integrity attestation (authoritative):** The local installer string can be spoofed on a rooted device, so back it with a server-side check. Request an integrity token from the Play Integrity API, send it to your backend, and verify on the server that `appRecognitionVerdict` is `PLAY_RECOGNIZED` and the device meets `MEETS_DEVICE_INTEGRITY`. A repackaged or sideloaded build will not be recognized by Play.

=== "Kotlin"
    ```kotlin
    val manager = IntegrityManagerFactory.create(context)
    manager.requestIntegrityToken(
        IntegrityTokenRequest.builder()
            .setNonce(serverProvidedNonce)
            .build()
    ).addOnSuccessListener { response ->
        // Send response.token() to your backend; never trust the verdict on-device.
        sendTokenToServer(response.token())
    }
    ```

**Additional hardening:**

- Treat the installer check as a hint and the server-verified Play Integrity verdict as the decision — never gate access on the on-device result alone.
- Implement the installer/source checks in native code (JNI) so the comparison and the allow-list cannot be trivially patched at the Java layer.
- Pair with APK signature verification so a re-signed repackaged build is rejected even if it spoofs the installer string.
- On a failed verdict, fail server-side: refuse to issue session tokens or unlock sensitive features rather than only showing a client-side warning.
