Implement certificate or public key pinning for all backend domains under the developer's control. Pin the leaf certificate or, preferably, the public key of the intermediate or root CA to avoid breakage on certificate renewal.

=== "Android (Network Security Config)"
    ```xml
    <!-- res/xml/network_security_config.xml -->
    <network-security-config>
        <domain-config>
            <domain includeSubdomains="true">api.example.com</domain>
            <pin-set expiration="2026-01-01">
                <!-- Primary public key pin (SHA-256 of SubjectPublicKeyInfo) -->
                <pin digest="SHA-256">AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=</pin>
                <!-- Backup pin — keep this on a different key/CA to allow rotation -->
                <pin digest="SHA-256">BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB=</pin>
            </pin-set>
        </domain-config>
    </network-security-config>
    ```
    Reference the config in `AndroidManifest.xml`:
    ```xml
    <application android:networkSecurityConfig="@xml/network_security_config" ...>
    ```

=== "Android (OkHttp)"
    ```kotlin
    val pinSet = CertificatePinner.Builder()
        .add("api.example.com", "sha256/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=")
        .add("api.example.com", "sha256/BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB=")
        .build()

    val client = OkHttpClient.Builder()
        .certificatePinner(pinSet)
        .build()
    ```

=== "iOS (NSPinnedDomains)"
    ```xml
    <!-- Info.plist -->
    <key>NSAppTransportSecurity</key>
    <dict>
        <key>NSPinnedDomains</key>
        <dict>
            <key>api.example.com</key>
            <dict>
                <key>NSIncludesSubdomains</key>
                <true/>
                <key>NSPinnedLeafIdentities</key>
                <array>
                    <dict>
                        <key>SPKI-SHA256-BASE64</key>
                        <string>AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=</string>
                    </dict>
                </array>
                <key>NSPinnedCAIdentities</key>
                <array>
                    <dict>
                        <key>SPKI-SHA256-BASE64</key>
                        <string>BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB=</string>
                    </dict>
                </array>
            </dict>
        </dict>
    </dict>
    ```

=== "iOS (TrustKit / URLSession)"
    ```swift
    import TrustKit

    let config: [String: Any] = [
        kTSKSwizzleNetworkDelegates: true,
        kTSKPinnedDomains: [
            "api.example.com": [
                kTSKIncludeSubdomains: true,
                kTSKPublicKeyHashes: [
                    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=",
                    "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB="
                ]
            ]
        ]
    ]
    TrustKit.initSharedInstance(withConfiguration: config)
    ```

**How to extract the public key pin:**
```bash
# From a live server
openssl s_client -connect api.example.com:443 -servername api.example.com 2>/dev/null \
  | openssl x509 -pubkey -noout \
  | openssl pkey -pubin -outform DER \
  | openssl dgst -sha256 -binary \
  | base64
```

Additional hardening recommendations:

- Always configure at least one backup pin on a different key or CA so you can rotate the primary pin without shipping an emergency update.
- Set an `expiration` date on Android pin-sets and monitor it — an expired pin-set is silently ignored, removing all protection.
- Validate pinning enforcement by running the app through a proxy (e.g., mitmproxy) after implementation; a correctly pinned app must fail to connect.
- Pin only domains under your control; exclude third-party SDKs and CDNs where you cannot guarantee certificate stability.
- Never rely solely on client-side pinning — complement it with short-lived tokens, server-side session validation, and anomaly detection on the backend.
