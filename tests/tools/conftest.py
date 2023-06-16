"""Fixtures for KB generator tests."""
import dataclasses
import os
from typing import Any

import pytest


@dataclasses.dataclass
class Message:
    message: dict[str, Any]


@dataclasses.dataclass
class GptResponse:
    choices: list[Message]


CONTENT = {
    "Vulnerability": {
        "Name": "Cross-Site Scripting (XSS)",
        "Description": "XSS is a type of security vulnerability that allows an attacker to inject malicious code into "
        "a web page viewed by other users. This can lead to theft of sensitive information, "
        "session hijacking, and other attacks.",
        "Sub-vulnerabilities": [
            {
                "Name": "Reflected XSS",
                "Description": "Reflected XSS occurs when user input is immediately returned to the user without being "
                "properly sanitized, allowing an attacker to inject malicious code that is executed in the "
                "user's browser.",
                "Examples": [
                    {
                        "Language": "Dart",
                        "Code": "import 'dart:html';\n\nvoid main() {\n  querySelector('#output').innerHtml = "
                        "window.location.search.substring(1);\n} ",
                    },
                    {
                        "Language": "Swift",
                        "Code": "import UIKit\nimport WebKit\n\nclass ViewController: UIViewController {\n    "
                        "@IBOutlet weak "
                        "var webView: WKWebView!\n    @IBOutlet weak var textField: UITextField!\n    \n    @IBAction "
                        "func goButtonPressed(_ sender: Any) {\n        let url = URL(string: "
                        '"https://example.com/search?q=\\(textField.text!)")!\n        let request = URLRequest('
                        "url: url)\n        webView.load(request)\n    }\n} ",
                    },
                    {
                        "Language": "Kotlin",
                        "Code": "import android.os.Bundle\nimport android.webkit.WebView\nimport "
                        "androidx.appcompat.app.AppCompatActivity\n\nclass MainActivity : AppCompatActivity() {\n    "
                        "override fun onCreate(savedInstanceState: Bundle?) {\n        super.onCreate("
                        "savedInstanceState)\n        setContentView(R.layout.activity_main)\n        \n        val "
                        "webView = findViewById<WebView>(R.id.webView)\n        val searchQuery = "
                        'intent.getStringExtra("search_query")\n        webView.loadUrl('
                        '"https://example.com/search?q=$searchQuery")\n    }\n} ',
                    },
                ],
            },
            {
                "Name": "Stored XSS",
                "Description": "Stored XSS occurs when user input is stored on the server and then displayed to other "
                "users without being properly sanitized, allowing an attacker to inject malicious code "
                "that is executed in the user's browser.",
                "Examples": [
                    {
                        "Language": "Dart",
                        "Code": "import 'dart:html';\n\nvoid main() {\n  querySelector('#submit').onClick.listen(("
                        "event) {\n "
                        "  final input = (querySelector('#input') as InputElement).value;\n    querySelector("
                        "'#output').innerHtml = input;\n  });\n} ",
                    },
                    {
                        "Language": "Swift",
                        "Code": "import UIKit\nimport WebKit\n\nclass ViewController: UIViewController {\n    "
                        "@IBOutlet weak "
                        "var webView: WKWebView!\n    @IBOutlet weak var textField: UITextField!\n    @IBOutlet weak "
                        "var submitButton: UIButton!\n    \n    @IBAction func submitButtonPressed(_ sender: Any) {\n "
                        '       let input = textField.text!\n        let script = "document.getElementById('
                        "'output').innerHTML = '\\(input)';\"\n        webView.evaluateJavaScript(script)\n    }\n} ",
                    },
                    {
                        "Language": "Kotlin",
                        "Code": "import android.os.Bundle\nimport android.webkit.WebView\nimport "
                        "androidx.appcompat.app.AppCompatActivity\n\nclass MainActivity : AppCompatActivity() {\n    "
                        "override fun onCreate(savedInstanceState: Bundle?) {\n        super.onCreate("
                        "savedInstanceState)\n        setContentView(R.layout.activity_main)\n        \n        val "
                        "webView = findViewById<WebView>(R.id.webView)\n        val submitButton = "
                        "findViewById<Button>(R.id.submitButton)\n        val input = findViewById<EditText>("
                        "R.id.input)\n        \n        submitButton.setOnClickListener {\n            val inputText "
                        '= input.text.toString()\n            val script = "document.getElementById('
                        "'output').innerHTML = '$inputText';\"\n            webView.evaluateJavascript(script, "
                        "null)\n        }\n    }\n} ",
                    },
                ],
            },
            {
                "Name": "DOM-based XSS",
                "Description": "DOM-based XSS occurs when user input is used to modify the DOM in a way that allows an "
                "attacker to inject malicious code that is executed in the user's browser.",
                "Examples": [
                    {
                        "Language": "Dart",
                        "Code": "import 'dart:html';\n\nvoid main() {\n  querySelector('#submit').onClick.listen(("
                        "event) {\n "
                        "  final input = (querySelector('#input') as InputElement).value;\n    querySelector("
                        "'#output').innerHtml = '<script>document.write(\"$input\")</script>';\n  });\n} ",
                    },
                    {
                        "Language": "Swift",
                        "Code": "import UIKit\nimport WebKit\n\nclass ViewController: UIViewController {\n    "
                        "@IBOutlet weak "
                        "var webView: WKWebView!\n    @IBOutlet weak var textField: UITextField!\n    @IBOutlet weak "
                        "var submitButton: UIButton!\n    \n    @IBAction func submitButtonPressed(_ sender: Any) {\n "
                        '       let input = textField.text!\n        let script = "document.getElementById('
                        "'output').innerHTML = '<script>document.write(\\\"\\(input)\\\")</script>';\"\n        "
                        "webView.evaluateJavaScript(script)\n    }\n} ",
                    },
                    {
                        "Language": "Kotlin",
                        "Code": "import android.os.Bundle\nimport android.webkit.WebView\nimport "
                        "androidx.appcompat.app.AppCompatActivity\n\nclass MainActivity : AppCompatActivity() {\n    "
                        "override fun onCreate(savedInstanceState: Bundle?) {\n        super.onCreate("
                        "savedInstanceState)\n        setContentView(R.layout.activity_main)\n        \n        val "
                        "webView = findViewById<WebView>(R.id.webView)\n        val submitButton = "
                        "findViewById<Button>(R.id.submitButton)\n        val input = findViewById<EditText>("
                        "R.id.input)\n        \n        submitButton.setOnClickListener {\n            val inputText "
                        '= input.text.toString()\n            val script = "document.getElementById('
                        "'output').innerHTML = '<script>document.write(\\\\\"$inputText\\\\\")</script>';\"\n         "
                        "   webView.evaluateJavascript(script, null)\n        }\n    }\n} ",
                    },
                ],
            },
        ],
    },
    "Meta": {
        "risk_rating": "high",
        "short_description": "XSS allows an attacker to inject malicious code into a web page viewed by other users.",
        "references": {
            "Reflected XSS (OWASP)": "https://owasp.org/www-community/attacks/xss/#reflected-xss",
            "Stored XSS (OWASP)": "https://owasp.org/www-community/attacks/xss/#stored-xss-attacks",
            "DOM-based XSS (OWASP)": "https://owasp.org/www-community/attacks/DOM_Based_XSS/",
        },
        "title": "Cross-Site Scripting (XSS)",
        "privacy_issue": False,
        "security_issue": True,
        "categories": {
            "OWASP_MASVS_L1": ["V2: Authentication and Session Management"],
            "OWASP_MASVS_L2": ["V2: Authentication and Session Management"],
        },
    },
    "Recommendation": {
        "Details": "To prevent XSS, user input should be properly sanitized before being displayed on a web page. "
        "This can be done by using a library or framework that automatically sanitizes user input, "
        "or by manually sanitizing user input using a whitelist of allowed characters.",
        "Code Fixes": [
            {
                "Name": "Reflected XSS",
                "Examples": [
                    {
                        "Language": "Dart",
                        "Code": "import 'package:html_unescape/html_unescape.dart';\nimport 'dart:html';\n\nvoid "
                        "main() {\n "
                        "querySelector('#output').innerHtml = HtmlUnescape().convert("
                        "window.location.search.substring(1));\n} ",
                    },
                    {
                        "Language": "Swift",
                        "Code": "import UIKit\nimport WebKit\n\nclass ViewController: UIViewController {\n    "
                        "@IBOutlet weak "
                        "var webView: WKWebView!\n    @IBOutlet weak var textField: UITextField!\n    \n    @IBAction "
                        "func goButtonPressed(_ sender: Any) {\n        let unescapedQuery = "
                        "textField.text!.removingPercentEncoding!\n        let url = URL(string: "
                        '"https://example.com/search?q=\\(unescapedQuery)")!\n        let request = URLRequest(url: '
                        "url)\n        webView.load(request)\n    }\n} ",
                    },
                    {
                        "Language": "Kotlin",
                        "Code": "import android.os.Bundle\nimport android.webkit.WebView\nimport "
                        "androidx.appcompat.app.AppCompatActivity\n\nclass MainActivity : AppCompatActivity() {\n    "
                        "override fun onCreate(savedInstanceState: Bundle?) {\n        super.onCreate("
                        "savedInstanceState)\n        setContentView(R.layout.activity_main)\n        \n        val "
                        "webView = findViewById<WebView>(R.id.webView)\n        val searchQuery = "
                        'intent.getStringExtra("search_query")?.replace("[^\u0000-\uffff]", "")\n        '
                        'webView.loadUrl("https://example.com/search?q=$searchQuery")\n    }\n} ',
                    },
                ],
            },
            {
                "Name": "Stored XSS",
                "Examples": [
                    {
                        "Language": "Dart",
                        "Code": "import 'package:html_unescape/html_unescape.dart';\nimport 'dart:html';\n\nvoid "
                        "main() {\n "
                        "querySelector('#submit').onClick.listen((event) {\n    final input = (querySelector("
                        "'#input') as InputElement).value;\n    querySelector('#output').innerHtml = HtmlEscape("
                        ").convert(input);\n  });\n} ",
                    },
                    {
                        "Language": "Swift",
                        "Code": "import UIKit\nimport WebKit\n\nclass ViewController: UIViewController {\n    "
                        "@IBOutlet weak "
                        "var webView: WKWebView!\n    @IBOutlet weak var textField: UITextField!\n    @IBOutlet weak "
                        "var submitButton: UIButton!\n    \n    @IBAction func submitButtonPressed(_ sender: Any) {\n "
                        '       let input = textField.text!.replacingOccurrences(of: "<", '
                        'with: "&lt;").replacingOccurrences(of: ">", with: "&gt;")\n        let script = '
                        "\"document.getElementById('output').innerHTML = '\\(input)';\"\n        "
                        "webView.evaluateJavaScript(script)\n    }\n} ",
                    },
                    {
                        "Language": "Kotlin",
                        "Code": "import android.os.Bundle\nimport android.webkit.WebView\nimport "
                        "androidx.appcompat.app.AppCompatActivity\n\nclass MainActivity : AppCompatActivity() {\n    "
                        "override fun onCreate(savedInstanceState: Bundle?) {\n        super.onCreate("
                        "savedInstanceState)\n        setContentView(R.layout.activity_main)\n        \n        val "
                        "webView = findViewById<WebView>(R.id.webView)\n        val submitButton = "
                        "findViewById<Button>(R.id.submitButton)\n        val input = findViewById<EditText>("
                        "R.id.input)\n        \n        submitButton.setOnClickListener {\n            val inputText "
                        '= input.text.toString().replace("<", "&lt;").replace(">", "&gt;")\n            val '
                        "script = \"document.getElementById('output').innerHTML = '$inputText';\"\n            "
                        "webView.evaluateJavascript(script, null)\n        }\n    }\n} ",
                    },
                ],
            },
            {
                "Name": "DOM-based XSS",
                "Examples": [
                    {
                        "Language": "Dart",
                        "Code": "import 'package:html_unescape/html_unescape.dart';\nimport 'dart:html';\n\nvoid "
                        "main() {\n "
                        "querySelector('#submit').onClick.listen((event) {\n    final input = (querySelector("
                        "'#input') as InputElement).value;\n    querySelector('#output').innerHtml = "
                        "'<script>document.write(\"' + HtmlEscape().convert(input) + '\")</script>';\n  });\n} ",
                    },
                    {
                        "Language": "Swift",
                        "Code": "import UIKit\nimport WebKit\n\nclass ViewController: UIViewController {\n    "
                        "@IBOutlet weak "
                        "var webView: WKWebView!\n    @IBOutlet weak var textField: UITextField!\n    @IBOutlet weak "
                        "var submitButton: UIButton!\n    \n    @IBAction func submitButtonPressed(_ sender: Any) {\n "
                        '       let input = textField.text!.replacingOccurrences(of: "<", '
                        'with: "&lt;").replacingOccurrences(of: ">", with: "&gt;")\n        let script = '
                        "\"document.getElementById('output').innerHTML = '<script>document.write(\\\"' + '\\(input)' "
                        "+ '\\\")</script>';\"\n        webView.evaluateJavaScript(script)\n    }\n} ",
                    },
                    {
                        "Language": "Kotlin",
                        "Code": "import android.os.Bundle\nimport android.webkit.WebView\nimport "
                        "androidx.appcompat.app.AppCompatActivity\n\nclass MainActivity : AppCompatActivity() {\n    "
                        "override fun onCreate(savedInstanceState: Bundle?) {\n        super.onCreate("
                        "savedInstanceState)\n        setContentView(R.layout.activity_main)\n        \n        val "
                        "webView = findViewById<WebView>(R.id.webView)\n        val submitButton = "
                        "findViewById<Button>(R.id.submitButton)\n        val input = findViewById<EditText>("
                        "R.id.input)\n        \n        submitButton.setOnClickListener {\n            val inputText "
                        '= input.text.toString().replace("<", "&lt;").replace(">", "&gt;")\n            val '
                        "script = \"document.getElementById('output').innerHTML = '<script>document.write(\\\\\"' + "
                        "'$inputText' + '\\\\\")</script>';\"\n            webView.evaluateJavascript(script, "
                        "null)\n        }\n    }\n} ",
                    },
                ],
            },
        ],
    },
}


@pytest.fixture
def gpt_response():
    return GptResponse(choices=[Message({"content": str(CONTENT)})])


def pytest_configure():
    os.environ["OPENAI_API_KEY"] = "mocked_value"
