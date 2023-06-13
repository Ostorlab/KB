### HTML Injection

HTML injection is a security vulnerability that arises when an input point in a web application can be manipulated by a user, enabling them to insert arbitrary HTML code into a susceptible web page. Exploiting this vulnerability can lead to various attacks, such as leaking a user's session cookies, which can then be exploited for more attacks. Furthermore, it allows the attacker to alter the content displayed to the victims, granting them the ability to modify the page to insert malicious code or deface the page with their own message.

**Code Examples:**

- Dart
```dart
import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';

class WebViewPage extends StatefulWidget {
  @override
  _WebViewPageState createState() => _WebViewPageState();
}

class _WebViewPageState extends State<WebViewPage> {
  WebViewController _webViewController;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('WebView'),
      ),
      body: WebView(
        initialUrl: 'https://example.com',
        onWebViewCreated: (WebViewController controller) {
          _webViewController = controller;
        },
      ),
      floatingActionButton: FloatingActionButton(
        child: Icon(Icons.add),
        onPressed: () {
          injectHTML();
        },
      ),
    );
  }

  void injectHTML() async {
    if (_webViewController != null) {
      await _webViewController.evaluateJavascript("""
        var element = document.createElement('div');
        element.innerHTML = '<h1>Injected HTML</h1>';
        document.body.appendChild(element);
      """);
    }
  }
}
```

- Kotlin:
```kotlin
import android.annotation.SuppressLint
import android.os.Bundle
import android.webkit.WebSettings
import android.webkit.WebView
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {

    private lateinit var webView: WebView

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        webView = findViewById(R.id.webView)

        val name = intent.getStringExtra("name")

        val html = "<html><body><h1>Hello, $name!</h1></body></html>"
        webView.loadDataWithBaseURL(null, html, "text/html", "UTF-8", null)

        val webSettings: WebSettings = webView.settings
        webSettings.javaScriptEnabled = true
    }
}
```

- Swift:
```swift
import UIKit
import WebKit

class ViewController: UIViewController, WKNavigationDelegate {
    
    private var webView: WKWebView!

    override func viewDidLoad() {
        super.viewDidLoad()
        
        webView = WKWebView(frame: view.bounds)
        webView.navigationDelegate = self
        view.addSubview(webView)
        
        let name = "John Doe"
        let html = "<html><body><h1>Hello, \(name)!</h1></body></html>"
        webView.loadHTMLString(html, baseURL: nil)
    }
}

```
