Implement anti-tampering as a layered release-build control, not as a single startup check. On iOS, the most practical baseline is:

1. Verify the integrity of the shipped executable and selected bundled resources.
2. Detect unexpected modification or repackaging and react safely.
3. Move high-value trust decisions to the server and use Apple App Attest where feasible.
4. Keep framework-specific code thin and place the actual integrity logic in the native iOS host app.

Local anti-tampering is a resilience control, not a complete security boundary. A determined attacker can often patch client-side checks, so sensitive authorization, entitlement, anti-fraud, and account-state decisions should still be enforced on the backend.

## Native iOS (Swift / Objective-C)

For native iOS applications, start with checks that are stable in production and do not rely on private APIs:

- hash the main executable or especially sensitive bundled resources,
- detect missing or altered files that should be present in the release build,
- run integrity checks at more than one point in the app lifecycle,
- and make the failure path meaningful for sensitive workflows.

### Swift example: verify the main executable hash

Store the expected hash in the release build pipeline and compare it at runtime:

```swift
import CryptoKit
import Foundation

enum IntegrityCheck {
    static func isMainExecutableIntact(expectedHash: String) -> Bool {
        guard let executablePath = Bundle.main.executablePath else {
            return false
        }

        let executableUrl = URL(fileURLWithPath: executablePath)
        guard let executableData = try? Data(contentsOf: executableUrl) else {
            return false
        }

        let digest = SHA256.hash(data: executableData)
        let actualHash = digest.map { String(format: "%02x", $0) }.joined()
        return actualHash == expectedHash.lowercased()
    }
}
```

### Swift example: verify a bundled resource

This is useful for sensitive configuration files, embedded rule sets, or model files that should not be silently replaced:

```swift
import CryptoKit
import Foundation

func isBundledResourceIntact(
    named resourceName: String,
    withExtension resourceExtension: String,
    expectedHash: String,
) -> Bool {
    guard let resourceUrl = Bundle.main.url(
        forResource: resourceName,
        withExtension: resourceExtension,
    ) else {
        return false
    }

    guard let resourceData = try? Data(contentsOf: resourceUrl) else {
        return false
    }

    let digest = SHA256.hash(data: resourceData)
    let actualHash = digest.map { String(format: "%02x", $0) }.joined()
    return actualHash == expectedHash.lowercased()
}
```

### Swift example: App Attest for server-backed integrity

Apple App Attest is stronger than a local-only check because the server can verify attestation material before trusting the app instance:

```swift
import CryptoKit
import DeviceCheck
import Foundation

@available(iOS 14.0, *)
enum AppAttestClient {
    static func generateKey() async throws -> String {
        let service = DCAppAttestService.shared
        guard service.isSupported else {
            throw NSError(domain: "AppAttest", code: 1)
        }

        return try await service.generateKey()
    }

    static func attestKey(
        keyIdentifier: String,
        challenge: Data,
    ) async throws -> Data {
        let clientDataHash = Data(SHA256.hash(data: challenge))
        return try await DCAppAttestService.shared.attestKey(
            keyIdentifier,
            clientDataHash: clientDataHash,
        )
    }
}
```

Use App Attest for server trust decisions such as issuing high-value session tokens, approving sensitive device bindings, or scoring fraud risk. Do not treat a successful local hash check as equivalent to server-verified attestation.

### Native iOS implementation advice

- Run checks in release builds and validate that debug-only shortcuts are not compiled into production.
- Check integrity again before sensitive actions such as payments, wallet operations, credential changes, or privileged API calls.
- Keep expected hashes or integrity values out of one easy-to-patch location.
- Log and monitor tamper events on the backend when the app is online.
- Prefer fail-closed behavior for sensitive features instead of only showing a warning.

## Flutter on iOS

Flutter can build an iOS archive directly, and Flutter also supports Dart obfuscation for iOS release targets. For anti-tampering, keep the enforcement logic in the native iOS host layer and call it from Dart only as a trigger or signal path.

### Build guidance

- Build the iOS release artifact with `flutter build ipa`.
- Consider `--obfuscate` and `--split-debug-info` for Dart code in release builds.
- Put the executable/resource integrity logic in the `ios/Runner` native project, not only in Dart.

### Dart example: invoke a native integrity check

```dart
import 'package:flutter/services.dart';

class AppIntegrity {
  static const MethodChannel _channel = MethodChannel('app.integrity');

  static Future<bool> isMainExecutableIntact(String expectedHash) async {
    final bool? intact = await _channel.invokeMethod<bool>(
      'isMainExecutableIntact',
      <String, Object>{
        'expectedHash': expectedHash,
      },
    );
    return intact ?? false;
  }
}
```

### Swift side of the Flutter bridge

```swift
import Flutter
import UIKit

@main
@objc final class AppDelegate: FlutterAppDelegate {
    override func application(
        _ application: UIApplication,
        didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
    ) -> Bool {
        let controller = window?.rootViewController as? FlutterViewController
        let channel = FlutterMethodChannel(
            name: "app.integrity",
            binaryMessenger: controller!.binaryMessenger
        )

        channel.setMethodCallHandler { call, result in
            guard call.method == "isMainExecutableIntact",
                  let arguments = call.arguments as? [String: Any],
                  let expectedHash = arguments["expectedHash"] as? String else {
                result(false)
                return
            }

            result(IntegrityCheck.isMainExecutableIntact(expectedHash: expectedHash))
        }

        return super.application(
            application,
            didFinishLaunchingWithOptions: launchOptions
        )
    }
}
```

### Flutter-specific advice

- Do not rely on Dart-only checks for tamper resistance.
- Keep symbol files produced by `--split-debug-info` outside the distributed app.
- Re-test the final `.ipa`, not only simulator builds.

## React Native on iOS

React Native release builds on iOS use the `Release` scheme and bundle JavaScript locally. Anti-tampering should live in the native iOS host app, because JavaScript-only checks are easier to patch after repackaging.

### JavaScript example: call a native module

```javascript
import { NativeModules } from 'react-native';

const { AppIntegrity } = NativeModules;

export async function isMainExecutableIntact(expectedHash) {
  const intact = await AppIntegrity.isMainExecutableIntact(expectedHash);
  return intact === true;
}
```

### React Native-specific advice

- Build and test with the Xcode `Release` scheme.
- Avoid leaving development toggles, debug logging, or dev endpoints accessible in production bundles.
- Put integrity checks in native Swift or Objective-C code and call them from JS only when needed.
- Reuse a shared native integrity helper rather than duplicating the logic in JavaScript.

## .NET MAUI on iOS

.NET MAUI apps should still enforce anti-tampering inside the iOS release build. You can implement the integrity check in platform-specific C# on iOS, or call native Apple APIs where needed.

### C# example: hash the main executable on iOS

```csharp
using System.Security.Cryptography;
using Foundation;

public static class AppIntegrity
{
    public static async Task<bool> IsMainExecutableIntactAsync(string expectedHash)
    {
        string? executablePath = NSBundle.MainBundle.ExecutablePath;
        if (string.IsNullOrEmpty(executablePath))
        {
            return false;
        }

        await using FileStream stream = File.OpenRead(executablePath);
        byte[] digest = await SHA256.HashDataAsync(stream);
        string actualHash = Convert.ToHexString(digest).ToLowerInvariant();

        return actualHash == expectedHash.ToLowerInvariant();
    }
}
```

### .NET MAUI-specific advice

- Publish and validate the iOS app in `Release` configuration.
- Keep integrity checks in iOS-specific code paths when they need Apple platform APIs.
- Re-test reflection-heavy, trimmed, or ahead-of-time compiled release builds after adding integrity controls.

## Capacitor on iOS

Capacitor uses a native iOS runtime and Xcode-managed host app, so the anti-tampering implementation should live in the iOS host project or a native Capacitor plugin.

### TypeScript example: register a plugin contract

```typescript
import { registerPlugin } from '@capacitor/core';

export interface AppIntegrityPlugin {
  checkIntegrity(options: { expectedHash: string }): Promise<{ intact: boolean }>;
}

export const AppIntegrity = registerPlugin<AppIntegrityPlugin>('AppIntegrity');
```

### TypeScript usage

```typescript
const result = await AppIntegrity.checkIntegrity({
  expectedHash: 'expected_sha256_here',
});

if (result.intact !== true) {
  throw new Error('App integrity validation failed.');
}
```

### Capacitor-specific advice

- Add the real integrity logic in the iOS plugin implementation, not only in TypeScript.
- Open the iOS project in Xcode and validate the final native release artifact.
- Re-check integrity after `npx cap sync ios` or major native plugin changes.

## Cordova on iOS

Cordova apps also end up as native iOS projects in Xcode. For anti-tampering, implement the detection in a native Cordova plugin and expose only a small JavaScript wrapper.

### JavaScript example: call a Cordova plugin

```javascript
function checkIntegrity(expectedHash) {
  return new Promise((resolve, reject) => {
    cordova.exec(
      resolve,
      reject,
      'AppIntegrity',
      'checkIntegrity',
      [expectedHash],
    );
  });
}
```

### Cordova-specific advice

- Do not keep the whole anti-tampering decision in the WebView layer.
- Validate the generated iOS workspace in Xcode before shipping.
- Re-run the checks after plugin, asset, or build-flag changes.

## Response strategy when tampering is detected

Choose a response that matches the business risk:

- block access to especially sensitive workflows,
- sign the user out and revoke locally cached privileged state,
- wipe or invalidate high-value secrets stored on device where appropriate,
- return the user to a safe screen instead of continuing normal execution,
- and notify the backend for correlation, fraud scoring, or incident investigation.

Avoid a response that only logs locally and keeps operating normally for privileged actions.

## Common mistakes to avoid

- Storing the expected hash as a single easy-to-edit plain-text constant.
- Running the check only once at startup.
- Relying only on JavaScript or Dart logic in hybrid frameworks.
- Treating anti-tampering as a substitute for backend authorization.
- Shipping release builds without validating the final `.ipa`.

## References

- OWASP MASTG - Testing File Integrity Checks (iOS): https://mas.owasp.org/MASTG/tests/ios/MASVS-RESILIENCE/MASTG-TEST-0090/
- OWASP MASVS - MASVS-RESILIENCE-1: https://mas.owasp.org/MASVS/controls/MASVS-RESILIENCE-1/
- Apple Developer - Establishing your app's integrity: https://developer.apple.com/documentation/devicecheck/establishing-your-app-s-integrity
- Flutter - Build and release an iOS app: https://docs.flutter.dev/deployment/ios
- Flutter - Obfuscate Dart code: https://docs.flutter.dev/deployment/obfuscate
- React Native - Publishing to Apple App Store: https://reactnative.dev/docs/publishing-to-app-store
- Microsoft Learn - Publish a .NET MAUI iOS app for App Store distribution: https://learn.microsoft.com/en-us/dotnet/maui/ios/deployment/publish-app-store?view=net-maui-9.0
- Capacitor iOS documentation: https://capacitorjs.com/docs/ios
- Apache Cordova iOS Platform Guide: https://cordova.apache.org/docs/en/latest/guide/platforms/ios/
