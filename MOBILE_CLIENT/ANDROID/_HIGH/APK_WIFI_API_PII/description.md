Android APK WiFi API allows access to Personal Identifiable Information (PII) such as network names and access points usage history, potentially leading to private data inference.

Applications using the `ACCESS_WIFI_STATE` permission and calling APIs like `getConnectionInfo` can access sensitive information about WiFi access points (such as BSSID, SSID, and RSSI) and potentially infer:"

* MAC Address which is a unique device identifier
* Geolocation data by using surrounding WiFi access points
* User movement history and social links inference relying on repeating patterns in WiFi access point usage

### Examples

=== "Java"

 ```java
 
    import android.content.Context;
    import android.net.wifi.WifiInfo;
    import android.net.wifi.WifiManager;
    
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
                
                System.out.println("SSID: " + ssid);
                System.out.println("BSSID: " + bssid);
                System.out.println("RSSI: " + rssi);
                System.out.println("MAC Address: " + macAddress);
                
                // Additional analysis could be performed here
                // such as inferring location or movement patterns
            } else {
                System.out.println("WiFi is not enabled");
            }
        }
    }
 ```

