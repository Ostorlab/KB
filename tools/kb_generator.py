"""Module responsible for interacting with the OpenAI API to generate KB entries."""
import ast
import dataclasses
import enum
import io
import json
import os
import pathlib
from typing import Any

import click
import openai
import tenacity
from openai import openai_object
from openai.api_resources import chat_completion


if "PROD" in os.environ:
    if "OPENAI_API_KEY" not in os.environ:
        raise ValueError("OPENAI_API_KEY is not defined")

    openai.api_key = os.getenv("OPENAI_API_KEY")
    MODEL_NAME = "gpt-3.5-turbo"


@dataclasses.dataclass
class RiskRating(enum.Enum):
    info = "INFO"
    hardening = "HARDENING"
    low = "LOW"
    medium = "MEDIUM"
    high = "HIGH"


@dataclasses.dataclass
class Platform(enum.Enum):
    ios = "IOS"
    android = "ANDROID"
    multi = "MULTIPLATFORM"
    common = "COMMON"
    web = "WEB"


@dataclasses.dataclass
class Vulnerability:
    name: str
    risk_rating: RiskRating
    platform: Platform


@dataclasses.dataclass
class KBEntry:
    description: str
    recommendation: str
    meta: dict[str, Any]
    vulnerability: Vulnerability | None = None


PLATFORM_TO_PATH = {
    "IOS": "MOBILE_CLIENT/IOS/",
    "ANDROID": "MOBILE_CLIENT/ANDROID/",
    "COMMON": "MOBILE_CLIENT/COMMON/",
    "MULTIPLATFORM": "MOBILE_CLIENT/MULTIPLATFORM_JS/",
    "WEB": "WEB_SERVICE/WEB/",
}


def dump_kb(kbentry: KBEntry) -> None:
    path_prefix = pathlib.Path(
        PLATFORM_TO_PATH[kbentry.vulnerability.platform],
        f"_{kbentry.vulnerability.risk_rating}",
    )

    path_prefix.mkdir(exist_ok=True, parents=True)

    with pathlib.Path(path_prefix, "description.md").open("w") as description_md:
        description_md.write(kbentry.description)

    with pathlib.Path(path_prefix, "recommendation.md").open("w") as recommendation_md:
        recommendation_md.write(kbentry.recommendation)

    with pathlib.Path(path_prefix, "meta.json").open("w") as meta_json:
        json.dump(kbentry.meta, meta_json)


def _ask_gpt(
    prompts: list[dict[str, str]], temperature: float = 0.0, max_tokens: int = 3200
) -> openai_object.OpenAIObject:
    """Send a prompt to OpenAI API."""
    gpt_response: openai_object.OpenAIObject = chat_completion.ChatCompletion.create(
        model=MODEL_NAME,
        temperature=temperature,
        max_tokens=max_tokens,
        messages=prompts,
    )
    return gpt_response


@tenacity.retry(
    stop=tenacity.stop_after_attempt(3),
    wait=tenacity.wait_fixed(2),
    retry=tenacity.retry_if_exception_type(),
)
def generate_kb(vulnerability: Vulnerability) -> KBEntry:
    """Send a prompt to the OpenAI API and generate KB.

    Args:
        vulnerability: Vulnerability object
    Returns:
        KBEntry

    """
    prompt_message = (
        f"KB entry for {vulnerability.name}, include vulnerable applications "
        "in Dart, Swift and Kotlin, reply strictly as valid JSON"
        "only use single quotes in code examples\n"
        """
        {
            "Vulnerability": {
                "Name": "[Vulnerability Name]",
                "Description": "[Vulnerability Description]".,
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
    gpt_response = _ask_gpt(prompts=prompts)
    content = gpt_response.choices[0].message["content"]
    try:
        response = json.loads(content)
    except ValueError:
        response = ast.literal_eval(content)
    # Vulnerability Description
    description_buffer = io.StringIO()
    vulnerability_data = response["Vulnerability"]
    vulnerability_name = vulnerability_data["Name"]
    vulnerability_description = vulnerability_data["Description"]
    description_buffer.write(f"# {vulnerability_name}\n\n")
    description_buffer.write(f"{vulnerability_description}\n\n")

    # Sub-vulnerabilities
    sub_vulnerabilities = vulnerability_data.get("Sub-vulnerabilities", [])
    for sub_vulnerability in sub_vulnerabilities:
        sub_vulnerability_name = sub_vulnerability["Name"]
        sub_vulnerability_description = sub_vulnerability["Description"]
        description_buffer.write(f"## {sub_vulnerability_name}\n\n")
        description_buffer.write(f"{sub_vulnerability_description}\n\n")
        # Code Examples
        examples = sub_vulnerability["Examples"]
        description_buffer.write("### Examples\n\n")
        for example in examples:
            language = example["Language"]
            code = example["Code"]
            description_buffer.write(f"#### {language}\n\n")
            description_buffer.write("```{language}\n")
            description_buffer.write(f"{code}\n")
            description_buffer.write("```\n\n")

    description_md = description_buffer.getvalue()

    # Recommendation
    recommendation_buffer = io.StringIO()
    recommendation_data = response["Recommendation"]
    recommendation_buffer.write("# Recommendation\n\n")
    recommendation_buffer.write(f"{recommendation_data['Details']}\n\n")
    code_fixes = recommendation_data.get("Code Fixes", [])
    for code_fix in code_fixes:
        code_fix_name = code_fix["Name"]
        examples = code_fix["Examples"]

        recommendation_buffer.write(f"## {code_fix_name}\n\n")
        for example in examples:
            language = example["Language"]
            code = example["Code"]

            recommendation_buffer.write(f"### {language}\n\n")
            recommendation_buffer.write("```{language}\n")
            recommendation_buffer.write(f"{code}\n")
            recommendation_buffer.write("```\n\n")

    recommendation_md = recommendation_buffer.getvalue()

    # Vulnerability metadata
    meta = response["Meta"]

    # KB Entry
    kbentry = KBEntry(description_md, recommendation_md, meta, vulnerability)

    return kbentry


@click.command()
@click.option("--name", prompt="Enter vulnerability name", help="Vulnerability name")
@click.option(
    "--risk",
    prompt="Enter risk rating",
    help="Risk rating",
    type=click.Choice([risk.value for risk in RiskRating], case_sensitive=False),
)
@click.option(
    "--platform",
    prompt="Enter platform",
    help="Platform",
    type=click.Choice([platform.value for platform in Platform], case_sensitive=False),
)
def main(name: str, risk: str, platform: str) -> None:
    vulnerability = Vulnerability(name, risk, platform)
    kbentry = generate_kb(vulnerability)
    dump_kb(kbentry)


if __name__ == "__main__":
    main()
