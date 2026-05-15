Implement runtime signature verification by comparing the APK signing certificate hash against a value hardcoded at build time.

```java
private boolean isSignatureValid(Context context) {
    try {
        PackageInfo info = context.getPackageManager().getPackageInfo(
            context.getPackageName(), PackageManager.GET_SIGNATURES);
        for (Signature sig : info.signatures) {
            MessageDigest md = MessageDigest.getInstance("SHA-256");
            md.update(sig.toByteArray());
            String actual = Base64.encodeToString(md.digest(), Base64.DEFAULT).trim();
            if (!EXPECTED_SIGNATURE.equals(actual)) return false;
        }
        return true;
    } catch (Exception e) {
        return false;
    }
}
```

Additional hardening recommendations:

- Move the check into a native (JNI) function to make static patching harder.
- Terminate or wipe sensitive state immediately on a failed check — do not degrade gracefully.
- Avoid storing `EXPECTED_SIGNATURE` as a plain string literal; obfuscate or derive it at runtime.
