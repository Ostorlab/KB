
# Android Wifi Api Information Disclosure Vulnerability

An information disclosure vulnerability in the Android WiFi API allows an attacker to access sensitive information such as network names and passwords, potentially leading to unauthorized access to WiFi networks and compromising user privacy.

Applications using the `ACESS_WIFI_STATE` interface and calling APIs like `getConnectionInfo` to access sensitive information about the WiFi access point, like `BSSID`, `SSID`, and `RSSI`,
can also allow for sensitive data inference:

    * MAC Address which is a unique device identifier
    * Geolocation data by using surrounding WiFi access points
    * User movement history and social links inference relying on repeating patterns in WiFi acces point usage

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

