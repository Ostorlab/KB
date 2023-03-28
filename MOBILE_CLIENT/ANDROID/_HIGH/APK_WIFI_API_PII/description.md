The application is using requesting the `ACCESS_WIFI_STATE` interface and calling APIs like `getConnectionInfo` to access sensitive information about the Wi-Fi access point, like BSSID, SSID, and RSSI, and about the device, like MAC address and IP address.

This API is known to be abused to access PII information like:

* Unique device identifier using the device's MAC address
* Geolocation data by using about surrounding Wi-Fi access points
* Travel history and social link by tracking users connecting to the same access points