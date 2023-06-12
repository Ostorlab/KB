"""Module responsible for interacting with the OpenAI API to generate KB entries."""
import json
import os
from typing import Any

import tenacity

import openai
from openai.api_resources import chat_completion
from openai import openai_object

if "OPENAI_API_KEY" not in os.environ:
    raise ValueError("OPENAI_API_KEY is not defined")

openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL_NAME = "gpt-3.5-turbo"

MOCK_DATA = {
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


def _write_to_md(data: dict[str, Any]) -> None:
    """Write to Markdown file"""

    # Vulnerability
    vulnerability = data["Vulnerability"]
    vulnerability_name = vulnerability["Name"]
    vulnerability_description = vulnerability["Description"]

    with open("description.md", "w") as f:
        f.write(f"# {vulnerability_name}\n\n")
        f.write(f"{vulnerability_description}\n\n")

        # Sub-vulnerabilities
        sub_vulnerabilities = vulnerability["Sub-vulnerabilities"]
        for sub_vulnerability in sub_vulnerabilities:
            sub_vulnerability_name = sub_vulnerability["Name"]
            sub_vulnerability_description = sub_vulnerability["Description"]

            f.write(f"## {sub_vulnerability_name}\n\n")
            f.write(f"{sub_vulnerability_description}\n\n")

            # Examples
            examples = sub_vulnerability["Examples"]
            f.write("### Examples\n\n")
            for example in examples:
                language = example["Language"]
                code = example["Code"]

                f.write(f"#### {language}\n\n")
                f.write("```{language}\n")
                f.write(f"{code}\n")
                f.write("```\n\n")

    # Recommendation
    recommendation = data["Recommendation"]
    recommendation_details = recommendation["Details"]

    with open("recommendation.md", "w") as f:
        f.write("# Recommendation\n\n")
        f.write(f"{recommendation_details}\n\n")

        # Code Fixes
        code_fixes = recommendation["Code Fixes"]
        for code_fix in code_fixes:
            code_fix_name = code_fix["Name"]
            examples = code_fix["Examples"]

            f.write(f"## {code_fix_name}\n\n")
            for example in examples:
                language = example["Language"]
                code = example["Code"]

                f.write(f"### {language}\n\n")
                f.write("```{language}\n")
                f.write(f"{code}\n")
                f.write("```\n\n")

    meta = data["Meta"]

    with open("meta.json", "w") as file:
        file.write(str(meta))


def _ask_the_wizard(
    prompts: list[dict[str, str]], temperature: float = 0.0, max_tokens: int = 3000
) -> openai_object.OpenAIObject:
    """Send a prompt to an OpenAI bot."""
    wizard_answer: openai_object.OpenAIObject = chat_completion.ChatCompletion.create(
        model=MODEL_NAME,
        temperature=temperature,
        max_tokens=max_tokens,
        messages=prompts,
    )
    return wizard_answer


@tenacity.retry(
    stop=tenacity.stop_after_attempt(3),
    wait=tenacity.wait_fixed(2),
    retry=tenacity.retry_if_exception_type(),
)
def generate_kb(vulnerability_name: str) -> dict[str, Any]:
    """Send a prompt to the OpenAI API.

    Args:
        vulnerability_name: vulnerability name
    Returns:

    """
    prompt_message = (
        f"Markdon KB entry for {vulnerability_name}, include vulnerable applications "
        "(complete code with imports) in Dart, Swift and Kotlin, reply as Markdown, use the following template\n"
        """
        {
            "Vulnerability": {
                "Name": "[Vulnerability Name]",
                "Description": "[Vulnerability Name], also known as [alternative name if applicable], " 
                        "is a [brief description of the vulnerability]. This vulnerability arises when "
                        "[describe the root cause or condition that leads to the vulnerability]".,
                "Sub-vulnerabilities": [
                    {
                        "Name": "[Sub-vulnerability Name]",
                        "Description": "[Description of the sub-vulnerability]"
                        "Examples": [
                            {
                                "Language": "Dart",
                                "Code": "[Dart vulnerable application]"
                            },
                            {
                                "Language": "Swift",
                                "Code": "[Swift vulnerable application]"
                            },
                            {
                                "Language": "Kotlin",
                                "Code": "[Kotlin vulnerable application]"
                            }
                        ]
                    },
                    {
                        "Name": "[Sub-vulnerability Name]",
                        "Description": "[Description of the sub-vulnerability]"
                        "Examples": [
                            {
                                "Language": "Dart",
                                "Code": "[Dart vulnerable application]"
                            },
                            {
                                "Language": "Swift",
                                "Code": "[Swift vulnerable application]"
                            },
                            {
                                "Language": "Kotlin",
                                "Code": "[Kotlin vulnerable application]"
                            }
                        ]
                    },
                    {
                        "Name": "[Sub-vulnerability Name]",
                        "Description": "[Description of the sub-vulnerability]"
                        "Examples": [
                            {
                                "Language": "Dart",
                                "Code": "[Dart vulnerable application]"
                            },
                            {
                                "Language": "Swift",
                                "Code": "[Swift vulnerable application]"
                            },
                            {
                                "Language": "Kotlin",
                                "Code": "[Kotlin vulnerable application]"
                            }
                        ]
                    }
                    ...
                ]
            },
            "Meta": {
              "risk_rating": "[info/hardening/low/medium/high]",
              "short_description": "[short_description]",
              "references": {
                "[Sub-vulnerability 1] (source name)": "[URL]",
                "[Sub-vulnerability 2] (source name)": "[URL]",
                "[Sub-vulnerability 3] (source name)": "[URL]"
              },
              "title": "[vulnerability title]",
              "privacy_issue": [true/false],
              "security_issue": [true/false],
              "categories": {
                "OWASP_MASVS_L1": [],
                "OWASP_MASVS_L2": []
              }
            },
            "Recommendation": {
                "Details": "[General Details]",
                "Code Fixes": [
                    {
                        "Name": "[Sub-vulnerability Name]",
                        "Examples": [
                            {
                                "Language": "Dart",
                                "Code": "[Dart vulnerable application]"
                            },
                            {
                                "Language": "Swift",
                                "Code": "[Swift vulnerable application]"
                            },
                            {
                                "Language": "Kotlin",
                                "Code": "[Kotlin vulnerable application]"
                            }
                        ]
                    }
                    ...
                ]
            }
        }
        """
    )

    prompts = [
        {
            "role": "user",
            "content": prompt_message,
        },
    ]

    wizard_answer = _ask_the_wizard(prompts=prompts).choices[0].message["content"]

    return json.loads(wizard_answer)


def main() -> None:
    vulnerability = input("Enter vulnerability name: ")
    kb = generate_kb(vulnerability)
    _write_to_md(kb)


if __name__ == "__main__":
    main()
