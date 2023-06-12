"""fixtures for kb generator tests"""
import pytest


@pytest.fixture
def json_output():
    return {
        "Vulnerability": {
            "Name": "HTML Injection",
            "Description": "HTML Injection, also known as Client-Side Injection, is a vulnerability that allows an attacker to inject malicious HTML code into a web page viewed by other users. This vulnerability arises when user input is not properly sanitized or validated before being displayed on a web page.",
            "Sub-vulnerabilities": [
                {
                    "Name": "Reflected HTML Injection",
                    "Description": "Reflected HTML Injection occurs when user input is immediately reflected back to the user without proper sanitization or validation. This can allow an attacker to inject malicious HTML code that will be executed by other users who view the page.",
                    "Examples": [
                        {
                            "Language": "Dart",
                            "Code": "import 'dart:io';\nimport 'dart:convert';\n\nvoid main() {\n  var request = await HttpClient().getUrl(Uri.parse('http://example.com')); // Make a GET request\n  var response = await request.close();\n  var responseBody = await response.transform(utf8.decoder).join();\n  print(responseBody);\n}",
                        },
                        {
                            "Language": "Swift",
                            "Code": 'import UIKit\nimport WebKit\n\nclass ViewController: UIViewController {\n    @IBOutlet weak var webView: WKWebView!\n    override func viewDidLoad() {\n        super.viewDidLoad()\n        let url = URL(string: "http://example.com")!\n        let request = URLRequest(url: url)\n        webView.load(request)\n    }\n}',
                        },
                        {
                            "Language": "Kotlin",
                            "Code": 'import android.os.Bundle\nimport android.webkit.WebView\nimport androidx.appcompat.app.AppCompatActivity\n\nclass MainActivity : AppCompatActivity() {\n    override fun onCreate(savedInstanceState: Bundle?) {\n        super.onCreate(savedInstanceState)\n        setContentView(R.layout.activity_main)\n        val myWebView: WebView = findViewById(R.id.webview)\n        myWebView.loadUrl("http://example.com")\n    }\n}',
                        },
                    ],
                },
                {
                    "Name": "Stored HTML Injection",
                    "Description": "Stored HTML Injection occurs when user input is stored on the server and displayed to other users without proper sanitization or validation. This can allow an attacker to inject malicious HTML code that will be executed by other users who view the page.",
                    "Examples": [
                        {
                            "Language": "Dart",
                            "Code": "import 'dart:io';\nimport 'dart:convert';\n\nvoid main() {\n  var request = await HttpClient().getUrl(Uri.parse('http://example.com')); // Make a GET request\n  var response = await request.close();\n  var responseBody = await response.transform(utf8.decoder).join();\n  // Store user input in database\n  var userInput = 'Hello, <script>alert(\"You have been hacked!\");</script> World!';\n  // Retrieve user input from database and display on web page\n  print(responseBody.replaceAll('{{userInput}}', userInput));\n}",
                        },
                        {
                            "Language": "Swift",
                            "Code": 'import UIKit\nimport WebKit\n\nclass ViewController: UIViewController {\n    @IBOutlet weak var webView: WKWebView!\n    override func viewDidLoad() {\n        super.viewDidLoad()\n        let url = URL(string: "http://example.com")!\n        let request = URLRequest(url: url)\n        webView.load(request)\n        // Store user input in database\n        let userInput = "Hello, <script>alert(\\"You have been hacked!\\");</script> World!"\n        // Retrieve user input from database and display on web page\n        let script = "document.getElementById(\\"userInput\\").innerHTML = \'\(userInput)\';"\n        webView.evaluateJavaScript(script, completionHandler: nil)\n    }\n}',
                        },
                        {
                            "Language": "Kotlin",
                            "Code": 'import android.os.Bundle\nimport android.webkit.WebView\nimport androidx.appcompat.app.AppCompatActivity\n\nclass MainActivity : AppCompatActivity() {\n    override fun onCreate(savedInstanceState: Bundle?) {\n        super.onCreate(savedInstanceState)\n        setContentView(R.layout.activity_main)\n        val myWebView: WebView = findViewById(R.id.webview)\n        myWebView.loadUrl("http://example.com")\n        // Store user input in database\n        val userInput = "Hello, <script>alert(\\"You have been hacked!\\");</script> World!"\n        // Retrieve user input from database and display on web page\n        myWebView.post { myWebView.evaluateJavascript("document.getElementById(\\"userInput\\").innerHTML = \'$userInput\';", null) }\n    }\n}',
                        },
                    ],
                },
            ],
        },
        "Meta": {
            "risk_rating": "high",
            "short_description": "HTML Injection allows an attacker to inject malicious HTML code into a web page viewed by other users.",
            "references": {
                "Reflected HTML Injection (OWASP)": "https://owasp.org/www-community/attacks/HTML_Injection",
                "Stored HTML Injection (OWASP)": "https://owasp.org/www-community/attacks/HTML_Injection",
            },
            "title": "HTML Injection",
            "privacy_issue": False,
            "security_issue": True,
            "categories": {
                "OWASP_MASVS_L1": ["V2: Authentication and Session Management"],
                "OWASP_MASVS_L2": ["V2: Authentication and Session Management"],
            },
        },
        "Recommendation": {
            "Details": "To prevent HTML Injection vulnerabilities, all user input should be properly sanitized and validated before being displayed on a web page. This can be done by using a server-side templating engine or by using a client-side library that automatically sanitizes user input.",
            "Code Fixes": [
                {
                    "Name": "Reflected HTML Injection",
                    "Examples": [
                        {
                            "Language": "Dart",
                            "Code": "import 'dart:io';\nimport 'dart:convert';\nimport 'package:html_unescape/html_unescape.dart';\n\nvoid main() {\n  var request = await HttpClient().getUrl(Uri.parse('http://example.com')); // Make a GET request\n  var response = await request.close();\n  var responseBody = await response.transform(utf8.decoder).join();\n  // Sanitize user input\n  var userInput = 'Hello, <script>alert(\"You have been hacked!\");</script> World!';\n  var sanitizedUserInput = HtmlUnescape().convert(userInput);\n  // Display sanitized user input on web page\n  print(responseBody.replaceAll('{{userInput}}', sanitizedUserInput));\n}",
                        },
                        {
                            "Language": "Swift",
                            "Code": 'import UIKit\nimport WebKit\n\nclass ViewController: UIViewController {\n    @IBOutlet weak var webView: WKWebView!\n    override func viewDidLoad() {\n        super.viewDidLoad()\n        let url = URL(string: "http://example.com")!\n        let request = URLRequest(url: url)\n        webView.load(request)\n        // Sanitize user input\n        let userInput = "Hello, <script>alert(\\"You have been hacked!\\");</script> World!"\n        let sanitizedUserInput = userInput.replacingOccurrences(of: "<", with: "&lt;").replacingOccurrences(of: ">", with: "&gt;")\n        // Display sanitized user input on web page\n        let script = "document.getElementById(\\"userInput\\").innerHTML = \'\(sanitizedUserInput)\';"\n        webView.evaluateJavaScript(script, completionHandler: nil)\n    }\n}',
                        },
                        {
                            "Language": "Kotlin",
                            "Code": 'import android.os.Bundle\nimport android.webkit.WebView\nimport androidx.appcompat.app.AppCompatActivity\n\nclass MainActivity : AppCompatActivity() {\n    override fun onCreate(savedInstanceState: Bundle?) {\n        super.onCreate(savedInstanceState)\n        setContentView(R.layout.activity_main)\n        val myWebView: WebView = findViewById(R.id.webview)\n        myWebView.loadUrl("http://example.com")\n        // Sanitize user input\n        val userInput = "Hello, <script>alert(\\"You have been hacked!\\");</script> World!"\n        val sanitizedUserInput = userInput.replace("<", "&lt;").replace(">", "&gt;")\n        // Display sanitized user input on web page\n        myWebView.post { myWebView.evaluateJavascript("document.getElementById(\\"userInput\\").innerHTML = \'$sanitizedUserInput\';", null) }\n    }\n}',
                        },
                    ],
                },
                {
                    "Name": "Stored HTML Injection",
                    "Examples": [
                        {
                            "Language": "Dart",
                            "Code": "import 'dart:io';\nimport 'dart:convert';\nimport 'package:html_unescape/html_unescape.dart';\n\nvoid main() {\n  var request = await HttpClient().getUrl(Uri.parse('http://example.com')); // Make a GET request\n  var response = await request.close();\n  var responseBody = await response.transform(utf8.decoder).join();\n  // Sanitize user input\n  var userInput = 'Hello, <script>alert(\"You have been hacked!\");</script> World!';\n  var sanitizedUserInput = HtmlUnescape().convert(userInput);\n  // Store sanitized user input in database\n  // Retrieve sanitized user input from database and display on web page\n  print(responseBody.replaceAll('{{userInput}}', sanitizedUserInput));\n}",
                        },
                        {
                            "Language": "Swift",
                            "Code": 'import UIKit\nimport WebKit\n\nclass ViewController: UIViewController {\n    @IBOutlet weak var webView: WKWebView!\n    override func viewDidLoad() {\n        super.viewDidLoad()\n        let url = URL(string: "http://example.com")!\n        let request = URLRequest(url: url)\n        webView.load(request)\n        // Sanitize user input\n        let userInput = "Hello, <script>alert(\\"You have been hacked!\\");</script> World!"\n        let sanitizedUserInput = userInput.replacingOccurrences(of: "<", with: "&lt;").replacingOccurrences(of: ">", with: "&gt;")\n        // Store sanitized user input in database\n        // Retrieve sanitized user input from database and display on web page\n        let script = "document.getElementById(\\"userInput\\").innerHTML = \'\(sanitizedUserInput)\';"\n        webView.evaluateJavaScript(script, completionHandler: nil)\n    }\n}',
                        },
                        {
                            "Language": "Kotlin",
                            "Code": 'import android.os.Bundle\nimport android.webkit.WebView\nimport androidx.appcompat.app.AppCompatActivity\n\nclass MainActivity : AppCompatActivity() {\n    override fun onCreate(savedInstanceState: Bundle?) {\n        super.onCreate(savedInstanceState)\n        setContentView(R.layout.activity_main)\n        val myWebView: WebView = findViewById(R.id.webview)\n        myWebView.loadUrl("http://example.com")\n        // Sanitize user input\n        val userInput = "Hello, <script>alert(\\"You have been hacked!\\");</script> World!"\n        val sanitizedUserInput = userInput.replace("<", "&lt;").replace(">", "&gt;")\n        // Store sanitized user input in database\n        // Retrieve sanitized user input from database and display on web page\n        myWebView.post { myWebView.evaluateJavascript("document.getElementById(\\"userInput\\").innerHTML = \'$sanitizedUserInput\';", null) }\n    }\n}',
                        },
                    ],
                },
            ],
        },
    }
