To restore server certificate validation, remove the custom trust manager entirely and rely on the platform's default trust evaluation whenever possible.

- **Use the default trust manager.** For ordinary HTTPS traffic, initialize the `SSLContext` with `null` (or with `TrustManagerFactory` seeded with `null`), which selects the platform's default trust manager and validates the server chain against the system's trusted CAs:

```java
SSLContext sslContext = SSLContext.getInstance("TLS");
sslContext.init(null, null, null); // platform default trust manager
connection.setSSLSocketFactory(sslContext.getSocketFactory());
```

- **If you need a custom trust manager, delegate to the platform default and only add restrictions.** A custom manager that needs to pin certificates or to add a private CA must still be able to reject a certificate: keep the delegating call to the platform's `checkServerTrusted` (which throws `CertificateException` on failure) or throw your own exception when the presented certificate does not match.

```java
public class PinningTrustManager implements X509TrustManager {
    @Override
    public void checkServerTrusted(X509Certificate[] chain, String authType)
            throws CertificateException {
        if (chain == null || chain.length == 0) {
            throw new CertificateException("empty certificate chain");
        }
        if (!matchesExpectedPin(chain[0])) {
            throw new CertificateException("certificate pin mismatch");
        }
    }
    // ...
}
```

- **Prefer the Android Network Security Configuration** over custom code when you need to trust an additional CA or to pin certificates for specific domains: it is declarative, reviewed by the platform, and cannot accidentally disable validation for every connection.

- **Never ship a trust-all manager for debugging.** Development-only trust managers frequently reach release builds. If local testing against self-signed certificates is unavoidable, gate the branch behind a debug-only flag and never enable `android:debuggable` in a released build.

- **Remember that `X509Certificate.checkValidity()` only checks expiry**, not the chain of trust: it is not a replacement for full validation.

For hostname verification (confirming that the certificate belongs to the host the app connected to), see the dedicated hostname validation entry: trusting the chain without verifying the hostname still allows machine-in-the-middle attacks with valid certificates for another domain.
