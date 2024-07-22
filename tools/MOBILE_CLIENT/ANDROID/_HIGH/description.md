
# Android Wifi Api Information Disclosure Vulnerability

An information disclosure vulnerability in the Android WiFi API allows an attacker to access sensitive information such as network names and passwords, potentially leading to unauthorized access to WiFi networks and compromising user privacy.

### Examples

#### Dart

```dart
dart
import 'package:flutter/material.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: Text('WiFi Info Vulnerability Demo'),
        ),
        body: Center(
          child: ElevatedButton(
            onPressed: () {
              // Vulnerable code
              var wifiInfo = WifiInfo();
              print('WiFi SSID: ${wifiInfo.getSSID()}');
              print('WiFi BSSID: ${wifiInfo.getBSSID()}');
            },
            child: Text('Get WiFi Info'),
          ),
        ),
      ),
    );
  }
}

class WifiInfo {
  String getSSID() {
    // Simulating fetching SSID from WiFi API
    return 'FakeSSID';
  }

  String getBSSID() {
    // Simulating fetching BSSID from WiFi API
    return 'FakeBSSID';
  }
}
```

#### Swift

```swift
swift
import Foundation

func main() {
    let userInput = readLine()
    print("Connecting to WiFi network: \(userInput ?? "Unknown")")
    // Vulnerable code that unintentionally leaks WiFi information
    let wifiInfo = try? String(contentsOf: URL(string: "http://example.com/wifi-info?network=\(userInput ?? "")")!)
    print("WiFi information: \(wifiInfo ?? "Unknown")")
}

main()
```

#### Kotlin

```kotlin
kotlin
import android.content.Context
import android.net.wifi.WifiManager

fun main() {
    val context: Context = TODO()
    val wifiManager = context.getSystemService(Context.WIFI_SERVICE) as WifiManager
    val wifiInfo = wifiManager.connectionInfo
    println("SSID: ${wifiInfo.ssid}")
    println("BSSID: ${wifiInfo.bssid}")
}
```
