**Unsafe custom trust evaluation** occurs when a custom `X509TrustManager` cannot reject an invalid server certificate through `checkServerTrusted`. It disables TLS certificate chain validation and exposes the app to machine-in-the-middle attacks.

Android apps can customize how TLS connections validate the server's certificate by providing their own trust manager, for example to pin certificates, to trust an additional private CA, or to work with self-signed certificates. The customization replaces the platform's chain-of-trust evaluation. An unsafe `checkServerTrusted` implementation cannot reject a certificate, most commonly because its body is empty or because it only logs. Every certificate chain is then accepted, including self-signed and expired certificates. Hostname verification is a separate check and must also remain enabled.

An attacker positioned on the same network (rogue access point, ARP spoofing, compromised router) can then run a machine-in-the-middle attack with any certificate: the app's `SSLContext` has been initialized with the unsafe trust manager, the handshake succeeds, and the attacker reads and modifies all of the traffic the app intended to protect with TLS, such as session tokens, credentials and personal data.

The vulnerable pattern is a class implementing `X509TrustManager` (or extending `X509ExtendedTrustManager`) whose `checkServerTrusted` override does not perform validation:

```java
TrustManager[] trustAllCerts = new TrustManager[] {
    new X509TrustManager() {
        @Override
        public void checkClientTrusted(X509Certificate[] chain, String authType) {
        }

        @Override
        public void checkServerTrusted(X509Certificate[] chain, String authType) {
            // accepts everything: no validation, no exception
        }

        @Override
        public X509Certificate[] getAcceptedIssuers() {
            return new X509Certificate[0];
        }
    }
};

SSLContext sslContext = SSLContext.getInstance("TLS");
sslContext.init(null, trustAllCerts, new SecureRandom());
connection.setSSLSocketFactory(sslContext.getSocketFactory());
```

Kotlin apps implement the same weakness with an anonymous object:

```kotlin
val trustAllCerts = arrayOf<TrustManager>(
    object : X509TrustManager {
        override fun checkClientTrusted(chain: Array<out X509Certificate>?, authType: String?) {}
        override fun checkServerTrusted(chain: Array<out X509Certificate>?, authType: String?) {}
        override fun getAcceptedIssuers(): Array<X509Certificate> = arrayOf()
    }
)
```

Any connection configured with such a trust manager accepts every server certificate, so the app is only reachable over TLS in name. The OWASP MASTG static test MASTG-TEST-0282 (Unsafe Custom Trust Evaluation) fails for these implementations, and the Android platform guidance calls the pattern an unsafe TrustManager: a trust manager that does not validate the certificate chain exposes the app to network attackers.
