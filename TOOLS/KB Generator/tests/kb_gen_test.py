import pytest


def test_generate_kb(json_output):
    assert isinstance(json_output, dict)

    vulnerability = json_output.get("Vulnerability")
    assert isinstance(vulnerability, dict)
    assert vulnerability["Name"] == "HTML Injection"
    assert (
        vulnerability["Description"]
        == "HTML Injection, also known as Client-Side Injection, is a vulnerability that allows "
        "an attacker to inject malicious HTML code into a web page viewed by other users. "
        "This vulnerability arises when user input is not properly sanitized or validated "
        "before being displayed on a web page."
    )

    sub_vulnerabilities = vulnerability.get("Sub-vulnerabilities", [])
    assert isinstance(sub_vulnerabilities, list)
    assert len(sub_vulnerabilities) > 0

    sub_vuln = sub_vulnerabilities[0]
    assert isinstance(sub_vuln, dict)
    assert sub_vuln["Name"] == "Reflected HTML Injection"
    assert (
        sub_vuln["Description"]
        == "Reflected HTML Injection occurs when user input is immediately reflected "
        "back to the user without proper sanitization or validation. "
        "This can allow an attacker to inject malicious HTML code "
        "that will be executed by other users who view the page."
    )

    examples = sub_vuln.get("Examples", [])
    assert isinstance(examples, list)
    assert len(examples) > 0

    example = examples[0]
    assert isinstance(example, dict)
    assert example["Language"] == "Dart"
    assert (
        example["Code"] == "import 'dart:io';\n"
        "import 'dart:convert';\n"
        "\n"
        "void main() {\n"
        "  var request = await HttpClient().getUrl(Uri.parse('http://example.com')); "
        "// Make a GET request\n"
        "  var response = await request.close();\n"
        "  var responseBody = await response.transform(utf8.decoder).join();\n"
        "  print(responseBody);\n"
        "}"
    )

    meta = json_output.get("Meta")
    assert isinstance(meta, dict)
    assert meta["risk_rating"] == "high"
    assert (
        meta["short_description"]
        == "HTML Injection allows an attacker to inject malicious HTML code into a web page viewed by other users."
    )
    assert meta["title"] == "HTML Injection"
    assert meta["privacy_issue"] is False
    assert meta["security_issue"] is True

    recommendation = json_output.get("Recommendation")
    assert isinstance(recommendation, dict)
    assert (
        recommendation["Details"]
        == "To prevent HTML Injection vulnerabilities, all user input should be properly sanitized and validated before being displayed on a web page. This can be done by using a server-side templating engine or by using a client-side library that automatically sanitizes user input."
    )

    code_fixes = recommendation.get("Code Fixes", [])
    assert isinstance(code_fixes, list)
    assert len(code_fixes) > 0

    code_fix = code_fixes[0]
    assert isinstance(code_fix, dict)
    assert code_fix["Name"] == "Reflected HTML Injection"

    examples = code_fix.get("Examples", [])
    assert isinstance(examples, list)
    assert len(examples) > 0

    example = examples[0]
    assert isinstance(example, dict)
    assert example["Language"] == "Dart"
    assert (
        example["Code"] == "import 'dart:io';\n"
        "import 'dart:convert';\n"
        "import 'package:html_unescape/html_unescape.dart';\n"
        "\n"
        "void main() {\n"
        "  var request = await HttpClient().getUrl(Uri.parse('http://example.com')); "
        "// Make a GET request\n"
        "  var response = await request.close();\n"
        "  var responseBody = await response.transform(utf8.decoder).join();\n"
        "  // Sanitize user input\n"
        '  var userInput = \'Hello, <script>alert("You have been hacked!");</script> '
        "World!';\n"
        "  var sanitizedUserInput = HtmlUnescape().convert(userInput);\n"
        "  // Display sanitized user input on web page\n"
        "  print(responseBody.replaceAll('{{userInput}}', sanitizedUserInput));\n"
        "}"
    )
