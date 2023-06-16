"""Fixtures for KB generator tests."""
import dataclasses
import os
from typing import Any


@dataclasses.dataclass
class Message:
    message: dict[str, Any]


@dataclasses.dataclass
class GptResponse:
    choices: list[Message]


KB_CONTENT = {
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

CODE_CONTENT = """
<data>
  <vulnerable_code>
    <Dart>
      import 'dart:io';
      import 'package:mysql1/mysql1.dart';

      Future<void> main() async {
        final conn = await MySqlConnection.connect(
          ConnectionSettings(
            host: 'localhost',
            port: 3306,
            user: 'root',
            password: 'password',
            db: 'test_db',
          ),
        );

        final userInput = stdin.readLineSync();
        final query = 'SELECT * FROM users WHERE id = $userInput';
        final results = await conn.query(query);

        for (final row in results) {
          print(row);
        }

        await conn.close();
      }
    </Dart>
    <Swift>
      import Foundation
      import MySQL

      let conn = try MySQL.Connection(
        host: "localhost",
        user: "root",
        password: "password",
        database: "test_db"
      )

      print("Enter user ID:")
      let userInput = readLine()!
      let query = "SELECT * FROM users WHERE id = (userInput)"
      let results = try conn.query(query)

      for row in results {
        print(row)
      }

      conn.close()
    </Swift>
    <Kotlin>
      import java.sql.DriverManager

      fun main() {
        val conn = DriverManager.getConnection(
          "jdbc:mysql://localhost:3306/test_db",
          "root",
          "password"
        )

        print("Enter user ID:")
        val userInput = readLine()!!
        val query = "SELECT * FROM users WHERE id = $userInput"
        val stmt = conn.createStatement()
        val results = stmt.executeQuery(query)

        while (results.next()) {
          println(results.getString("username"))
        }

        conn.close()
      }
    </Kotlin>
  </vulnerable_code>
  <patched_code>
    <Dart>
      import 'dart:io';
      import 'package:mysql1/mysql1.dart';

      Future<void> main() async {
        final conn = await MySqlConnection.connect(
          ConnectionSettings(
            host: 'localhost',
            port: 3306,
            user: 'root',
            password: 'password',
            db: 'test_db',
          ),
        );

        final userInput = stdin.readLineSync();
        final query = 'SELECT * FROM users WHERE id = ?';
        final results = await conn.query(query, [userInput]);

        for (final row in results) {
          print(row);
        }

        await conn.close();
      }
    </Dart>
    <Swift>
      import Foundation
      import MySQL

      let conn = try MySQL.Connection(
        host: "localhost",
        user: "root",
        password: "password",
        database: "test_db"
      )

      print("Enter user ID:")
      let userInput = readLine()!
      let query = "SELECT * FROM users WHERE id = ?"
      let results = try conn.query(query, [userInput])

      for row in results {
        print(row)
      }

      conn.close()
    </Swift>
    <Kotlin>
      import java.sql.DriverManager

      fun main() {
        val conn = DriverManager.getConnection(
          "jdbc:mysql://localhost:3306/test_db",
          "root",
          "password"
        )

        print("Enter user ID:")
        val userInput = readLine()!!
        val query = "SELECT * FROM users WHERE id = ?"
        val pstmt = conn.prepareStatement(query)
        pstmt.setString(1, userInput)
        val results = pstmt.executeQuery()

        while (results.next()) {
          println(results.getString("username"))
        }

        conn.close()
      }
    </Kotlin>
  </patched_code>
</data>
"""


def pytest_configure():
    os.environ["OPENAI_API_KEY"] = "mocked_value"


def mock_chat_completion_create(**kwargs):
    prompt = kwargs["messages"][0]["content"]

    if prompt.startswith("KB entry for"):
        return GptResponse(choices=[Message({"content": str(KB_CONTENT)})])
    else:
        return GptResponse(choices=[Message({"content": CODE_CONTENT})])


def validate_json_format(json_data):
    # Check if the JSON data is a dictionary
    assert isinstance(json_data, dict), "JSON data must be a dictionary."

    # Check if the required keys are present
    required_keys = ["risk_rating", "short_description", "references", "title"]
    for key in required_keys:
        assert key in json_data, f"Required key '{key}' is missing in JSON data."

    # Check the data types and formats of the keys
    assert isinstance(json_data["risk_rating"], str), "risk_rating must be a string."
    assert isinstance(
        json_data["short_description"], str
    ), "short_description must be a string."
    assert isinstance(json_data["references"], dict), "references must be a dictionary."
    assert isinstance(json_data["title"], str), "title must be a string."

    # Check the format of the references
    references = json_data["references"]
    assert isinstance(references, dict), "references must be a dictionary."
