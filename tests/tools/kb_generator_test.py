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
    kbentry = kb_generator.generate_kb("HTML Injection")

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
