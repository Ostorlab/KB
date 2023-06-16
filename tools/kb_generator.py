"""Module responsible for interacting with the OpenAI API to generate KB entries."""
import ast
import dataclasses
import enum
import io
import json
import logging
import os
import pathlib
from typing import Any
import bs4

import click
import openai
import tenacity
from openai import openai_object
from openai.api_resources import chat_completion

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = "gpt-3.5-turbo"

KB_JSON_TEMPLATE = """
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
                                "Code": "[TODO]"
                            },
                            {
                                "Language": "Swift",
                                "Code": "[TODO]"
                            },
                            {
                                "Language": "Kotlin",
                                "Code": "[TODO]"
                            }
                        ]
                    },
                    {
                        "Name": "[Sub-vulnerability Name]",
                        "Description": "[Description of the sub-vulnerability]"
                        "Examples": [
                            {
                                "Language": "Dart",
                                "Code": "[TODO]"
                            },
                            {
                                "Language": "Swift",
                                "Code": "[TODO]"
                            },
                            {
                                "Language": "Kotlin",
                                "Code": "[TODO]"
                            }
                        ]
                    },
                    {
                        "Name": "[Sub-vulnerability Name]",
                        "Description": "[Description of the sub-vulnerability]"
                        "Examples": [
                            {
                                "Language": "Dart",
                                "Code": "[TODO]"
                            },
                            {
                                "Language": "Swift",
                                "Code": "[TODO]"
                            },
                            {
                                "Language": "Kotlin",
                                "Code": "[TODO]"
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
                "Details": "[Recommendation Details]",
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

CODE_XML_TEMPLATE = """
<data>
  <vulnerable_code>
    <Dart>Dart vulnerable application Code</Dart>
    <Swift>Swift vulnerable application code</Swift>
    <Kotlin>Kotlin vulnerable application code</Kotlin>
  </vulnerable_code>
  <patched_code>
    <Dart>Dart patched application Code</Dart>
    <Swift>Swift patched application code</Swift>
    <Kotlin>Kotlin patched application code</Kotlin>
  </patched_code>
</data>
"""


@dataclasses.dataclass
class RiskRating(enum.Enum):
    """RiskRating dataclass"""

    INFO = "INFO"
    HARDENING = "HARDENING"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


@dataclasses.dataclass
class Platform(enum.Enum):
    """Platform dataclass"""

    IOS = "IOS"
    ANDROID = "ANDROID"
    MULTI = "MULTIPLATFORM"
    COMMON = "COMMON"
    WEB = "WEB"


@dataclasses.dataclass
class Vulnerability:
    """Vulnerability dataclass"""

    name: str
    risk_rating: RiskRating
    platform: Platform


@dataclasses.dataclass
class KBEntry:
    """KBEntry dataclass"""

    description: str
    recommendation: str
    meta: dict[str, Any]
    vulnerability: Vulnerability


PLATFORM_TO_PATH = {
    "IOS": "MOBILE_CLIENT/IOS/",
    "ANDROID": "MOBILE_CLIENT/ANDROID/",
    "COMMON": "MOBILE_CLIENT/COMMON/",
    "MULTIPLATFORM": "MOBILE_CLIENT/MULTIPLATFORM_JS/",
    "WEB": "WEB_SERVICE/WEB/",
}


def dump_kb(kbentry: KBEntry) -> pathlib.Path:
    """Dump KB entry into files.

    Args:
        kbentry: KBEntry object
    Returns:

    """
    path_prefix = pathlib.Path(
        PLATFORM_TO_PATH[kbentry.vulnerability.platform.value],
        f"_{kbentry.vulnerability.risk_rating.value}",
    )

    path_prefix.mkdir(exist_ok=True, parents=True)

    with pathlib.Path(path_prefix, "description.md").open(
        "w", encoding="utf-8"
    ) as description_md:
        description_md.write(kbentry.description)

    with pathlib.Path(path_prefix, "recommendation.md").open(
        "w", encoding="utf-8"
    ) as recommendation_md:
        recommendation_md.write(kbentry.recommendation)

    with pathlib.Path(path_prefix, "meta.json").open(
        "w", encoding="utf-8"
    ) as meta_json:
        json.dump(kbentry.meta, meta_json, indent=4)

    return path_prefix


def _ask_gpt(
    prompts: list[dict[str, str]], temperature: float = 0.0, max_tokens: int = 3200
) -> openai_object.OpenAIObject:
    """Send a prompt to OpenAI API."""
    if OPENAI_API_KEY is None:
        raise ValueError

    openai.api_key = OPENAI_API_KEY
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
        vulnerability: a vulnerability object
    Returns:
        KB entry

    """
    prompt_message = (
        f"KB entry for {vulnerability.name}, reply strictly as valid JSON"
        f"{KB_JSON_TEMPLATE}"
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

    subvulnz = response["Vulnerability"].get("Sub-vulnerabilities", [])
    recommendations = response["Recommendation"]
    if vulnerability.platform == Platform.WEB:
        target = "Web"
    else:
        target = "Mobile"
    for idx in range(len(subvulnz)):
        subvuln_name = subvulnz[idx]["Name"]
        prompt_message = (
            f"Complete {target} application code that is vulnerable to {subvuln_name} in Dart, Swift, Kotlin "
            f"use the following template {CODE_XML_TEMPLATE}"
        )

        prompts = [
            {
                "role": "user",
                "content": prompt_message,
            },
        ]
        gpt_response = _ask_gpt(prompts=prompts)
        content = gpt_response.choices[0].message["content"]

        parsed_content = bs4.BeautifulSoup(content, features="lxml")
        vulnerable_code = parsed_content.find("vulnerable_code")
        patched_code = parsed_content.find("patched_code")

        if vulnerable_code is None or patched_code is None:
            continue

        dart_code = vulnerable_code.find("dart")
        subvulnz[idx]["Examples"][0]["Code"] = (
            dart_code.text if dart_code and hasattr(dart_code, "text") else "[TODO]"
        )
        swift_code = vulnerable_code.find("swift")
        subvulnz[idx]["Examples"][1]["Code"] = (
            swift_code.text if swift_code and hasattr(swift_code, "text") else "[TODO]"
        )
        kotlin_code = vulnerable_code.find("kotlin")
        subvulnz[idx]["Examples"][2]["Code"] = (
            kotlin_code.text
            if kotlin_code and hasattr(kotlin_code, "text")
            else "[TODO]"
        )

        dart_code = patched_code.find("dart")
        recommendations["Code Fixes"][idx]["Examples"][0]["Code"] = (
            dart_code.text if dart_code and hasattr(dart_code, "text") else "[TODO]"
        )
        swift_code = patched_code.find("swift")
        recommendations["Code Fixes"][idx]["Examples"][1]["Code"] = (
            swift_code.text if swift_code and hasattr(swift_code, "text") else "[TODO]"
        )
        kotlin_code = patched_code.find("kotlin")
        recommendations["Code Fixes"][idx]["Examples"][2]["Code"] = (
            kotlin_code.text
            if kotlin_code and hasattr(kotlin_code, "text")
            else "[TODO]"
        )

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
            description_buffer.write(f"```{language}\n")
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
    """
    Entry point of the program.

    This function executes the main logic of the program, including initialization,
    user interactions, and finalization steps. It serves as the starting point for
    running the application.

    Args:
        name: vulnerability name
        risk: vulnerability risk rating
        platform: vulnerability target platform
    Returns:

    """
    vulnerability = Vulnerability(name, RiskRating(risk), Platform(platform))
    kbentry = generate_kb(vulnerability)
    output_path = dump_kb(kbentry)
    logging.info(output_path)


if __name__ == "__main__":
    main()
