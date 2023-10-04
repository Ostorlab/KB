To mitigate the risks associated with HTML injection vulnerabilities, the following recommendations should be implemented:

- Sanitize User Input: Perform proper input validation and sanitization on user-supplied data that will be rendered as part of HTML code. Use encoding techniques to ensure that user input is treated as data and not executable code.

- Use Templating Engines: Utilize secure templating engines or frameworks that automatically escape user input by default, such as Handlebars, Twig, or Django templates. These engines help prevent HTML injection by properly handling user input.

- Whitelisting Input: Implement whitelisting or allow listing approaches to validate and restrict input for HTML elements, attributes, and protocols. Only allow specific tags, attributes, and protocols that are necessary for the application's functionality.

- Contextual Output Encoding: Encode user-generated content based on its context. Different contexts, such as HTML attributes, JavaScript code, or CSS styles, require specific encoding techniques to prevent HTML injection attacks. Use appropriate encoding functions or libraries based on the context.

=== "Dart"
	```dart
	import 'package:flutter/material.dart';
	import 'package:webview_flutter/webview_flutter.dart';
	import 'package:sanitize_html/sanitize_html.dart' show sanitizeHtml;
	
	void main() => runApp(MyApp());
	
	class MyApp extends StatelessWidget {
	  @override
	  Widget build(BuildContext context) {
	    return MaterialApp(
	      title: 'HTML Injection Demo',
	      theme: ThemeData(
	        primarySwatch: Colors.blue,
	      ),
	      home: WebViewScreen(),
	    );
	  }
	}
	
	class WebViewScreen extends StatefulWidget {
	  @override
	  _WebViewScreenState createState() => _WebViewScreenState();
	}
	
	class _WebViewScreenState extends State<WebViewScreen> {
	  late WebViewController _webViewController;
	  String? htmlInput;
	
	  @override
	  void initState() {
	    super.initState();
	    getHtmlInputFromIntent();
	  }
	
	  void getHtmlInputFromIntent() {
	    // Retrieve the intent extras
	    Map<String, dynamic>? extras =
	        ModalRoute.of(context)?.settings.arguments as Map<String, dynamic>?;
	
	    // Extract the user input from the intent extras
	    htmlInput = extras?['htmlInput'];
	  }
	
	  void _injectHtml() async {
	    if (htmlInput != null) {
	      final sanitizedHtml = sanitizeHtml(htmlInput);
	      await _webViewController.loadUrl(
	        Uri.dataFromString(sanitizedHtml, mimeType: 'text/html', encoding: Encoding.getByName('utf-8'))!.toString(),
	      );
	    }
	  }
	
	
	  @override
	  Widget build(BuildContext context) {
	    return Scaffold(
	      appBar: AppBar(
	        title: Text('HTML Injection Demo'),
	      ),
	      body: Column(
	        children: [
	          ElevatedButton(
	            onPressed: _injectHtml,
	            child: Text('Inject HTML'),
	          ),
	          Expanded(
	            child: WebView(
	              initialUrl: 'about:blank',
	              onWebViewCreated: (WebViewController controller) {
	                _webViewController = controller;
	              },
	            ),
	          ),
	        ],
	      ),
	    );
	  }
	}
	```


=== "Swift"
	```Swift
	import UIKit
	import WebKit
	import DOMPurify
	
	class ViewController: UIViewController, WKNavigationDelegate {
	    
	    private var webView: WKWebView!
	
	    override func viewDidLoad() {
	        super.viewDidLoad()
	        
	        webView = WKWebView(frame: view.bounds)
	        webView.navigationDelegate = self
	        view.addSubview(webView)
	        
	        let name = "John Doe"
	        let plainText = "Hello, \(name)!"
	        let sanitizedText = sanitizeHTML(plainText)
	        let html = "<html><body><h1>\(sanitizedText)</h1></body></html>"
	        webView.loadHTMLString(html, baseURL: nil)
	    }
	    
	    private func sanitizeHTML(_ html: String) -> String {
	        guard let sanitized = DOMPurify.sanitize(html) else {
	            return ""
	        }
	        return sanitized
	    }
	}
	```



=== "Kotlin"
	```kotlin
	import android.annotation.SuppressLint
	import android.os.Bundle
	import android.webkit.WebSettings
	import android.webkit.WebView
	import androidx.appcompat.app.AppCompatActivity
	
	class MainActivity : AppCompatActivity() {
	
	    private lateinit var webView: WebView
	
	    PolicyFactory policy = new HtmlPolicyBuilder()
	        .allowElements("a")
	        .allowUrlProtocols("https")
	        .allowAttributes("href").onElements("a")
	        .requireRelNofollowOnLinks()
	        .build();
	
	    override fun onCreate(savedInstanceState: Bundle?) {
	        super.onCreate(savedInstanceState)
	        setContentView(R.layout.activity_main)
	
	        webView = findViewById(R.id.webView)
	
	        val name = intent.getStringExtra("name")
	        val sanitizedName = policy.sanitize(name)   
	
	        val html = "<html><body><h1>Hello, $sanitizedName!</h1></body></html>"
	        webView.loadDataWithBaseURL(null, html, "text/html", "UTF-8", null)
	
	        val webSettings: WebSettings = webView.settings
	        webSettings.javaScriptEnabled = false
	    }
	
	}
	```
