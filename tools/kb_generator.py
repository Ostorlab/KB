"""Module responsible for interacting with the OpenAI API to generate KB entries."""
import json
import os
from typing import Any

import tenacity

import openai
from openai.api_resources import chat_completion
from openai import openai_object

if os.getenv("DEV") is not None:
    if "OPENAI_API_KEY" not in os.environ:
        raise ValueError("OPENAI_API_KEY is not defined")

    openai.api_key = os.getenv("OPENAI_API_KEY")
    MODEL_NAME = "gpt-3.5-turbo"


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
        sub_vulnerabilities = vulnerability.get("Sub-vulnerabilities", [])
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
        code_fixes = recommendation.get("Code Fixes", [])
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
    """Send a prompt to OpenAI API."""
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
    """Send a prompt to the OpenAI API and generate KB.

    Args:
        vulnerability_name: vulnerability name
    Returns:

    """
    prompt_message = (
        f"KB entry for {vulnerability_name}, include vulnerable applications "
        "(complete code with imports) in Dart, Swift and Kotlin, reply as JSON\n"
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

    wizard_answer = _ask_the_wizard(prompts=prompts).choices[0].message["content"]

    return json.loads(wizard_answer)


def main() -> None:
    vulnerability = input("Enter vulnerability name: ")
    kb = generate_kb(vulnerability)
    _write_to_md(kb)


if __name__ == "__main__":
    main()
