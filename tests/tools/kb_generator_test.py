"""Unittests for KB generator."""

import os.path
from typing import Any

import pytest
import tenacity
from pyfakefs import fake_filesystem
from pytest_mock import plugin

from tests import utils
from tools import kb_generator


def _mock_create(**kwargs: Any) -> utils.MockResponse:
    """Adapt the chat completion create kwargs to the shared prompt mock."""
    return utils.mock_chat_completion_create(prompts=kwargs["messages"])


def testGenerateKB_whenVulnerabilityProvided_returnsKBEntry(
    mocker: plugin.MockerFixture,
) -> None:
    """generate_kb is responsible for generating KB entries from a vulnerability name.
    when provided with a valid vulnerability name, this function should return a dict
    representing a KB entry
    """
    mocker.patch(
        "tools.kb_generator._ask_gpt",
        side_effect=utils.mock_chat_completion_create,
    )
    vulnerability = kb_generator.Vulnerability(
        "Sql Injection", kb_generator.RiskRating.HIGH, kb_generator.Platform.WEB
    )

    kbentry = kb_generator.generate_kb(vulnerability)

    assert (
        "SQL injection is a type of security vulnerability that allows an attacker to inject malicious SQL "
        "statements into an application's database" in kbentry.description
    )
    assert "import 'package:sqflite/sqflite.dart';" in kbentry.description
    assert (
        "it is important to use parameterized queries or prepared statements instead of concatenating user input "
        "directly into SQL statements. " in kbentry.recommendation
    )
    assert kbentry.meta["risk_rating"] == "high"
    assert (
        kbentry.meta["short_description"]
        == "SQL Injection vulnerability allows an attacker to execute malicious SQL "
        "queries to the database,potentially gaining access to sensitive data or "
        "performing unauthorized actions."
    )
    assert kbentry.meta["references"] == {
        "NIST": "https://nvd.nist.gov/vuln/detail/CVE-2019-16759",
        "OWASP ": "https: //owasp.org/www-community/attacks/SQL_Injection",
        "SANS": "https://www.sans.org/top-25-software-errors/#cat3",
    }
    assert kbentry.meta["title"] == "SQL Injection Vulnerability"
    assert kbentry.meta["security_issue"] is True
    assert kbentry.meta["privacy_issue"] is False
    assert kbentry.meta["categories"] == {
        "OWASP_MASVS_L1": [
            "V2: Authentication and Session Management",
            "V3: Cryptography",
            "V4: Network Communication",
            "V5: Platform Interaction",
            "V6: Code Quality and Build Settings",
        ],
        "OWASP_MASVS_L2": ["V7: Data Protection", "V8: Resilience Against Attack"],
    }


def testGenerateKB_whenFireworksProviderProvided_generatesKBEntryUsingFireworks(
    mocker: plugin.MockerFixture,
) -> None:
    """generate_kb with the fireworks provider calls the Fireworks inference endpoint."""
    openai_client_mock = mocker.patch("tools.kb_generator.OpenAI")
    openai_client_mock.return_value.chat.completions.create.side_effect = _mock_create
    mocker.patch.dict(os.environ, {"FIREWORKS_API_KEY": "fw-test-key"})
    vulnerability = kb_generator.Vulnerability(
        "Sql Injection", kb_generator.RiskRating.HIGH, kb_generator.Platform.WEB
    )

    kbentry = kb_generator.generate_kb(
        vulnerability, kb_generator.LLMProvider.FIREWORKS
    )

    _, client_kwargs = openai_client_mock.call_args
    assert client_kwargs["api_key"] == "fw-test-key"
    assert client_kwargs["base_url"] == "https://api.fireworks.ai/inference/v1"

    _, create_kwargs = openai_client_mock.return_value.chat.completions.create.call_args
    assert create_kwargs["model"] == "accounts/fireworks/models/llama-v3p3-70b-instruct"
    assert kbentry.meta["risk_rating"] == "high"
    assert kbentry.meta["title"] == "SQL Injection Vulnerability"


def testGenerateKB_whenDefaultProviderProvided_generatesKBEntryUsingOpenRouter(
    mocker: plugin.MockerFixture,
) -> None:
    """generate_kb with the default provider calls the OpenRouter endpoint."""
    openai_client_mock = mocker.patch("tools.kb_generator.OpenAI")
    openai_client_mock.return_value.chat.completions.create.side_effect = _mock_create
    vulnerability = kb_generator.Vulnerability(
        "Sql Injection", kb_generator.RiskRating.HIGH, kb_generator.Platform.WEB
    )

    kbentry = kb_generator.generate_kb(vulnerability)

    _, client_kwargs = openai_client_mock.call_args
    assert client_kwargs["base_url"] == "https://openrouter.ai/api/v1"

    _, create_kwargs = openai_client_mock.return_value.chat.completions.create.call_args
    assert create_kwargs["model"] == "gpt-3.5-turbo"
    assert kbentry.meta["risk_rating"] == "high"


def testGenerateKB_whenFireworksApiKeyIsMissing_raisesValueError(
    mocker: plugin.MockerFixture,
) -> None:
    """generate_kb with the fireworks provider and no API key raises a ValueError."""
    mocker.patch("tools.kb_generator.OpenAI")
    mocker.patch("tenacity.nap.sleep")
    mocker.patch.dict(os.environ, {}, clear=False)
    os.environ.pop("FIREWORKS_API_KEY", None)
    vulnerability = kb_generator.Vulnerability(
        "Sql Injection", kb_generator.RiskRating.HIGH, kb_generator.Platform.WEB
    )

    with pytest.raises(tenacity.RetryError) as excinfo:
        kb_generator.generate_kb(vulnerability, kb_generator.LLMProvider.FIREWORKS)

    last_exception = excinfo.value.last_attempt.exception()
    assert isinstance(last_exception, ValueError) is True
    assert "FIREWORKS_API_KEY" in str(last_exception)


def testDumpKB_whenPathIsValid_writesFiles(
    mocker: plugin.MockerFixture, fs: fake_filesystem.FakeFilesystem
) -> None:
    """Test creation of KB files."""
    vulnerability = kb_generator.Vulnerability(
        name="XSS",
        platform=kb_generator.Platform.WEB,
        risk_rating=kb_generator.RiskRating.HIGH,
    )
    kbentry = kb_generator.KBEntry(
        vulnerability=vulnerability,
        description="Description",
        recommendation="Recommendation",
        meta={"Meta": "Meta data"},
    )
    kb_generator.dump_kb(kbentry)

    assert os.path.exists("WEB_SERVICE/WEB/_HIGH") is True
    assert os.path.exists("WEB_SERVICE/WEB/_HIGH/description.md") is True
    assert os.path.exists("WEB_SERVICE/WEB/_HIGH/recommendation.md") is True
    assert os.path.exists("WEB_SERVICE/WEB/_HIGH/meta.json") is True
