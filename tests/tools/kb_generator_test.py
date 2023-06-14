"""Unittests for KB generator."""
from pytest_mock import plugin

from tests.tools import conftest
from tools import kb_generator


def testGenerateKB_whenVulnerabilityProvided_returnskbentry(
    mocker: plugin.MockerFixture, wizard_response: conftest.WizardResponse
):
    """generate_kb is responsible for generating KB entries from a vulnerability name.
    when provided with a valid vulnerability name, this function should return a dict
    representing a KB entry
    """
    mocker.patch("tools.kb_generator._ask_the_wizard", return_value=wizard_response)
    vulnerability = kb_generator.Vulnerability("XSS", "HIGH", "WEB")
    kbentry = kb_generator.generate_kb(vulnerability)

    assert (
        "XSS is a type of security vulnerability that allows an attacker to inject malicious code into a web page viewed by other users"
        in kbentry.description
    )
    assert (
        "This can lead to theft of sensitive information, session hijacking, and other attacks"
        in kbentry.description
    )
    assert (
        "Reflected XSS occurs when user input is immediately returned to the user without being properly sanitized"
        in kbentry.description
    )
    assert (
        "Stored XSS occurs when user input is stored on the server and then displayed to other users without being properly sanitized"
        in kbentry.description
    )
    assert (
        "DOM-based XSS occurs when user input is used to modify the DOM in a way that allows an attacker to inject malicious code"
        in kbentry.description
    )
    assert (
        "To prevent XSS, user input should be properly sanitized before being displayed on a web page"
        in kbentry.recommendation
    )
    assert kbentry.meta["risk_rating"] == "high"
    assert (
        kbentry.meta["short_description"]
        == "XSS allows an attacker to inject malicious code into a web page viewed by other users."
    )
    assert kbentry.meta["references"] == {
        "Reflected XSS (OWASP)": "https://owasp.org/www-community/attacks/xss/#reflected-xss",
        "Stored XSS (OWASP)": "https://owasp.org/www-community/attacks/xss/#stored-xss-attacks",
        "DOM-based XSS (OWASP)": "https://owasp.org/www-community/attacks/DOM_Based_XSS/",
    }
    assert kbentry.meta["title"] == "Cross-Site Scripting (XSS)"
    assert kbentry.meta["security_issue"] is True
    assert kbentry.meta["privacy_issue"] is False
    assert kbentry.meta["categories"] == {
        "OWASP_MASVS_L1": ["V2: Authentication and Session Management"],
        "OWASP_MASVS_L2": ["V2: Authentication and Session Management"],
    }
