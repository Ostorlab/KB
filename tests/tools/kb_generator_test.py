"""Unittests for KB generator."""
from typing import Any
from pytest_mock import plugin
from tools import kb_generator


def testGenerateKB_whenVulnerabilityProvided_returnsKB(
    mocker: plugin.MockerFixture, json_output: dict[str, Any]
):
    """generate_kb is responsible for generating KB entries from a vulnerability name.
    when provided with a valid vulnerability name, this function should return a dict
    representing a KB entry
    """
    mocker.patch("tools.kb_generator.generate_kb", return_value=json_output)
    kb_output = kb_generator.generate_kb("HTML Injection")
    vulnerability = kb_output.get("Vulnerability")

    assert vulnerability["Name"] == "Cross-Site Scripting (XSS)"
    assert (
        vulnerability["Description"]
        == "XSS is a type of security vulnerability that allows an attacker to inject "
        "malicious code into a web page viewed by other users. This can lead to theft "
        "of sensitive information, session hijacking, and other attacks."
    )

    sub_vulnerabilities = vulnerability.get("Sub-vulnerabilities", [])
    assert isinstance(sub_vulnerabilities, list)
    assert len(sub_vulnerabilities) > 0

    sub_vuln = sub_vulnerabilities[0]
    assert isinstance(sub_vuln, dict)
    assert sub_vuln["Name"] == "Reflected XSS"
    assert (
        sub_vuln["Description"]
        == "Reflected XSS occurs when user input is immediately returned to the user "
        "without being properly sanitized, allowing an attacker to inject malicious "
        "code that is executed in the user's browser."
    )

    examples = sub_vuln.get("Examples", [])
    assert isinstance(examples, list)
    assert len(examples) > 0

    example = examples[0]
    assert isinstance(example, dict)
    assert example["Language"] == "Dart"
    assert (
        example["Code"] == "import 'dart:html';\n"
        "\n"
        "void main() {\n"
        "  querySelector('#output').innerHtml = window.location.search.substring(1);\n"
        "}"
    )

    meta = json_output.get("Meta")
    assert isinstance(meta, dict)
    assert meta["risk_rating"] == "high"
    assert (
        meta["short_description"]
        == "XSS allows an attacker to inject malicious code into a web page viewed by "
        "other users."
    )
    assert meta["title"] == "Cross-Site Scripting (XSS)"
    assert meta["privacy_issue"] is False
    assert meta["security_issue"] is True

    recommendation = json_output.get("Recommendation")
    assert isinstance(recommendation, dict)
    assert (
        recommendation["Details"]
        == "To prevent XSS, user input should be properly sanitized before being "
        "displayed on a web page. This can be done by using a library or framework "
        "that automatically sanitizes user input, or by manually sanitizing user "
        "input using a whitelist of allowed characters."
    )

    code_fixes = recommendation.get("Code Fixes", [])
    assert isinstance(code_fixes, list)
    assert len(code_fixes) > 0

    code_fix = code_fixes[0]
    assert isinstance(code_fix, dict)
    assert code_fix["Name"] == "Reflected XSS"

    examples = code_fix.get("Examples", [])
    assert isinstance(examples, list)
    assert len(examples) > 0

    example = examples[0]
    assert isinstance(example, dict)
    assert example["Language"] == "Dart"
    assert (
        example["Code"] == "import 'package:html_unescape/html_unescape.dart';\n"
        "import 'dart:html';\n"
        "\n"
        "void main() {\n"
        "  querySelector('#output').innerHtml = "
        "HtmlUnescape().convert(window.location.search.substring(1));\n"
        "}"
    )
