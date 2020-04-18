Apache Cordova below version 3.5.0 suffers from multiple vulnerabilties:

* Apache Cordova Android before 3.5.1 allows remote attackers to change the start page via a crafted intent URL
* Phonegap whitelisting can be bypassed by an attacker by using Websockets through Webview
* Apache Cordova Android before 3.5.1 allows remote attackers to bypass the HTTP whitelist and connect to arbitrary servers by using JavaScript to open WebSocket connections through WebView
* Javascript can also be executed by loading a malicious site by starting an application with errorurl set to the malicious site
* Phonegap whitelisting can be bypassed by an attacker. For example, if foo.com is whitelisted, foo.com.evil.com will pass the check.