# Mitigating WiFi API Privacy Risks

To mitigate the privacy risks associated with mobile WiFi APIs' access to Personal Identifiable Information (PII), both users and developers can take several precautions:

## For Users:

* Keep the mobile operating system and all apps updated to the latest versions.
* Be cautious about granting WiFi-related permissions to apps.
* Use a VPN when connecting to public WiFi networks.
* Regularly review app permissions in device settings.

## For Developers:

* Request explicit user permission for accessing sensitive WiFi information.
* Implement the principle of 'Least Privilege', only requesting and using the minimum permissions necessary for the app to function.
* Hash or anonymize any WiFi data before storing or transmitting it.
* Provide clear privacy policies explaining how WiFi information is used.
* Consider whether WiFi information is truly necessary for app functionality.

### Code Examples for Developers:

=== "Android"

  ```java
  // Request appropriate permissions
  if (ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION)
      != PackageManager.PERMISSION_GRANTED) {
      ActivityCompat.requestPermissions(this,
             new String[]{Manifest.permission.ACCESS_FINE_LOCATION},
             PERMISSION_REQUEST_CODE);
  }

  // Use Android 10+ methods whenever possible
  if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
      // Use Android 10+ compliant methods
      // For example, WifiInfo.getSSID() and getBSSID() return masked values by default
  } else {
      // Use methods for earlier Android versions
  }

  // Use privacy focused NetworkCallback API
  ConnectivityManager connectivityManager = 
      (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);

  NetworkRequest.Builder builder = new NetworkRequest.Builder();
  builder.addTransportType(NetworkCapabilities.TRANSPORT_WIFI);

  connectivityManager.registerNetworkCallback(builder.build(), new ConnectivityManager.NetworkCallback() {
      @Override
      public void onAvailable(Network network) {
          // Handle WiFi connection here without accessing PII
      }
  });
  ```

=== "iOS"

  ```swift
  // First, ensure you have proper permissions in Info.plist
  // <key>NSLocationWhenInUseUsageDescription</key>
  // <string>This app needs to access your location to find nearby WiFi networks</string>
  
  import NetworkExtension
  
  func requestWiFiPermission() {
      // Request permission before accessing WiFi information
      if #available(iOS 13.0, *) {
          NEHotspotHelper.register(options: nil, queue: .main) { (cmd) -> Void in
              // Handle commands appropriately
              print("Permission request processed")
          }
      }
  }
  
  // Use minimal WiFi information when necessary
  func connectToKnownNetwork() {
      // Instead of collecting and storing SSID/BSSID pairs,
      // use the system's built-in capabilities
      if let configuration = NEHotspotConfiguration(ssid: "KnownNetwork") {
          NEHotspotConfigurationManager.shared.apply(configuration) { error in
              if let error = error {
                  print("Error connecting: \(error.localizedDescription)")
              } else {
                  print("Connected successfully")
              }
          }
      }
  }
  
  // If you must access WiFi information, anonymize it
  func getAnonymizedWifiInfo() -> String? {
      guard let interfaces = CNCopySupportedInterfaces() as? [String],
            let interface = interfaces.first,
            let networkInfo = CNCopyCurrentNetworkInfo(interface as CFString) as? [String: Any],
            let ssid = networkInfo[kCNNetworkInfoKeySSID as String] as? String else {
          return nil
      }
      
      // Hash the SSID instead of using it directly
      return ssid.data(using: .utf8)?.sha256Hash.hexString
  }
  
  // Extension for hashing
  extension Data {
      var sha256Hash: Data {
          var hash = [UInt8](repeating: 0, count: Int(CC_SHA256_DIGEST_LENGTH))
          self.withUnsafeBytes {
              _ = CC_SHA256($0.baseAddress, CC_LONG(self.count), &hash)
          }
          return Data(hash)
      }
      
      var hexString: String {
          return map { String(format: "%02hhx", $0) }.joined()
      }
  }
  ```
