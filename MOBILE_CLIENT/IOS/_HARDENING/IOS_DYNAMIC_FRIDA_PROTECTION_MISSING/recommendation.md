Implement Frida detection as a layered runtime resilience control, not as a single startup check.

On iOS, the practical goal is not to make instrumentation impossible, but to reliably detect common Frida-based runtime tampering attempts and react safely during sensitive flows. A strong baseline is:

1. Detect suspicious dynamic libraries, images, threads, ports, or runtime state associated with Frida or Frida Gadget.
2. Re-run checks during sensitive workflows instead of only once at launch.
3. Keep the detection logic in the native iOS layer, not only in Flutter, React Native, or other cross-platform code.
4. Move high-value trust decisions to the backend and combine local signals with Apple App Attest where feasible.

Local Frida detection is a resilience signal, not a complete security boundary. A determined attacker may still patch or bypass client-side checks, so account actions, entitlements, payment approval, fraud decisions, and other high-value operations should still be verified server-side.

## Native iOS (Swift / Objective-C)

For native iOS applications, prefer multiple independent checks instead of one signature match. A single string like `frida` is easy to patch around.

### Swift example: inspect loaded images for Frida-related artifacts

This is useful for detecting Frida Gadget or other obviously named injected components loaded into the current process:

```swift
import Foundation
import MachO

enum FridaDetection {
    private static let suspiciousImageMarkers = [
        "frida",
        "gadget",
        "gum-js-loop",
        "frida-agent",
        "frida-gadget",
    ]

    static func hasSuspiciousLoadedImage() -> Bool {
        let imageCount = _dyld_image_count()

        for index in 0..<imageCount {
            guard let imageName = _dyld_get_image_name(index) else {
                continue
            }

            let path = String(cString: imageName).lowercased()
            if suspiciousImageMarkers.contains(where: { path.contains($0) }) {
                return true
            }
        }

        return false
    }
}
```

### Swift example: probe common local instrumentation ports

This is a heuristic, not a standalone control. It can help detect common listener setups when instrumentation exposes a predictable loopback endpoint:

```swift
import Darwin
import Foundation

func isLocalPortOpen(_ port: UInt16) -> Bool {
    let socketFd = socket(AF_INET, SOCK_STREAM, 0)
    if socketFd < 0 {
        return false
    }
    defer { close(socketFd) }

    var address = sockaddr_in()
    address.sin_len = UInt8(MemoryLayout<sockaddr_in>.size)
    address.sin_family = sa_family_t(AF_INET)
    address.sin_port = port.bigEndian
    address.sin_addr = in_addr(s_addr: inet_addr("127.0.0.1"))

    let result = withUnsafePointer(to: &address) {
        $0.withMemoryRebound(to: sockaddr.self, capacity: 1) {
            connect(socketFd, $0, socklen_t(MemoryLayout<sockaddr_in>.size))
        }
    }

    return result == 0
}
```

Use this as one signal among several. Port-based detection alone is fragile because ports can be changed, blocked, or proxied.

### Swift example: centralize the decision

Combine multiple signals and run the check again before sensitive operations:

```swift
import Foundation

enum RuntimeProtection {
    static func isInstrumentationDetected() -> Bool {
        if FridaDetection.hasSuspiciousLoadedImage() is true {
            return true
        }

        if isLocalPortOpen(27042) is true {
            return true
        }

        if isLocalPortOpen(27043) is true {
            return true
        }

        return false
    }
}
```

### Native iOS implementation advice

- Run checks from native iOS code. Cross-platform code can call into native logic, but the actual detection should stay in Swift, Objective-C, or native libraries.
- Re-run detection before sensitive actions such as authentication completion, wallet access, payment approval, key export, or privileged API calls.
- Avoid keeping all detection strings or decision logic in one obvious place.
- Treat detection as a signal to fail closed for high-value flows, clear sensitive in-memory state, and report telemetry when appropriate.
- Test on real release builds, not only debug or simulator builds.

## Apple App Attest for server-backed trust

Use local Frida detection together with backend trust validation when possible. Apple App Attest gives the server stronger evidence about the app instance than a local-only runtime check.

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

Use App Attest results on the server to gate high-value operations. Local anti-instrumentation checks should complement this, not replace it.

## Flutter on iOS

For Flutter, keep Frida detection in the native iOS host app and expose only a thin bridge to Dart.

```dart
import 'package:flutter/services.dart';

class RuntimeProtection {
  static const MethodChannel _channel = MethodChannel('app.runtime_protection');

  static Future<bool> isInstrumentationDetected() async {
    final bool? detected = await _channel.invokeMethod<bool>(
      'isInstrumentationDetected',
    );
    return detected == true;
  }
}
```

Swift side:

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
            name: "app.runtime_protection",
            binaryMessenger: controller!.binaryMessenger
        )

        channel.setMethodCallHandler { call, result in
            guard call.method == "isInstrumentationDetected" else {
                result(false)
                return
            }

            result(RuntimeProtection.isInstrumentationDetected())
        }

        return super.application(
            application,
            didFinishLaunchingWithOptions: launchOptions
        )
    }
}
```

Flutter-specific advice:

- Do not rely on Dart-only anti-instrumentation logic.
- Re-test the final signed `.ipa`.
- Keep the response to detection in native code for sensitive flows when possible.

## React Native on iOS

For React Native, place the actual detection logic in the native iOS host layer or a native module, and expose only a minimal JavaScript-facing API.

```javascript
import { NativeModules } from 'react-native';

const { RuntimeProtection } = NativeModules;

export async function isInstrumentationDetected() {
  const detected = await RuntimeProtection.isInstrumentationDetected();
  return detected === true;
}
```

React Native-specific advice:

- Keep the important checks outside JavaScript.
- Re-run the detection around sensitive workflows, not only during app boot.
- Avoid leaving verbose debug behavior in production builds that helps an attacker inspect the app state.

## Capacitor and other hybrid iOS stacks

For Capacitor or similar hybrid runtimes, implement Frida detection in the iOS host app or a native plugin and use the web layer only as a consumer of the result.

## Additional hardening guidance

- Use more than one detection path. Loaded-image checks, runtime heuristics, and backend integrity signals are stronger together than separately.
- Validate how the app behaves after detection. For high-risk actions, prefer blocking the action instead of only showing a warning.
- Keep analytics around detection events so repeated instrumented sessions can be correlated server-side.
- Periodically re-evaluate the implementation against current Frida and Frida Gadget workflows.
