# HTML Injection
To mitigate the risks associated with HTML injection vulnerabilities, the following recommendations should be implemented:

- Sanitize User Input: Perform proper input validation and sanitization on user-supplied data that will be rendered as part of HTML code. Use encoding techniques to ensure that user input is treated as data and not executable code.

- Use Templating Engines: Utilize secure templating engines or frameworks that automatically escape user input by default, such as Handlebars, Twig, or Django templates. These engines help prevent HTML injection by properly handling user input.

- Whitelisting Input: Implement whitelisting or allow listing approaches to validate and restrict input for HTML elements, attributes, and protocols. Only allow specific tags, attributes, and protocols that are necessary for the application's functionality.

- Contextual Output Encoding: Encode user-generated content based on its context. Different contexts, such as HTML attributes, JavaScript code, or CSS styles, require specific encoding techniques to prevent HTML injection attacks. Use appropriate encoding functions or libraries based on the context.

- Content Security Policy (CSP): Implement and enforce a Content Security Policy for your web application. CSP helps mitigate HTML injection by specifying which sources of content (e.g., scripts, styles, images) are allowed to be loaded and executed on a webpage.

**Code Examples:**

- Dart
```dart
import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';
import 'package:html/parser.dart' show parse;

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
          injectPlainText();
        },
      ),
    );
  }

  void injectPlainText() async {
    if (_webViewController != null) {
      String plainText = 'Injected HTML';
      String encodedText = parse(plainText).outerHtml;
      await _webViewController.evaluateJavascript("""
        var element = document.createElement('div');
        element.textContent = '$encodedText';
        document.body.appendChild(element);
      """);
    }
  }
}

```

- Kotlin
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

        val plainText = "Hello, $name!"
        val encodedText = android.text.Html.escapeHtml(plainText)
        val html = "<html><body><h1>$encodedText</h1></body></html>"
        webView.loadDataWithBaseURL(null, html, "text/html", "UTF-8", null)

        val webSettings: WebSettings = webView.settings
        webSettings.javaScriptEnabled = true
    }
}

```

- Swift
```Swift
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
        let plainText = "Hello, \(name)!"
        let encodedText = plainText.addingPercentEncoding(withAllowedCharacters: .alphanumerics) ?? ""
        let html = "<html><body><h1>\(encodedText)</h1></body></html>"
        webView.loadHTMLString(html, baseURL: nil)
    }
}
```