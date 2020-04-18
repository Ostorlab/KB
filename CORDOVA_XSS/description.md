Mobile Cross-Site Scripting (XSS) attacks are a type of injection, in which malicious scripts are injected into otherwise benign and trusted content. XSS attacks occur when an attacker can inject malicious code through:

*   Untrusted Inter-Process Communication (IPC) input
*   Man-in-the-Middle attack
*   Untrusted content stored on the webserver application
*   Untrusted local file input

Example script to test presence of XSS

```html
<script>alert("Ostorlab XSS!")</script>
```

```html
<img src="http://ostorlab.co/js_xss2" onerror=alert(document.cookie)>
```

XSS vulnerabilities for Cordova applications are critical as they allow access to native functionality on the target
phone and could lead to unauthorized access to contacts, messages, camera, audio and location.
