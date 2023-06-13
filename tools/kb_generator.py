"""Module responsible for interacting with the OpenAI API to generate KB entries."""
import json
import os

import tenacity
import dataclasses
import dataclass_csv
import io

import openai
from openai.api_resources import chat_completion
from openai import openai_object

if os.getenv("DEV") is not None:
    if "OPENAI_API_KEY" not in os.environ:
        raise ValueError("OPENAI_API_KEY is not defined")

    openai.api_key = os.getenv("OPENAI_API_KEY")
    MODEL_NAME = "gpt-3.5-turbo"


@dataclasses.dataclass
class Vulnerability:
    name: str
    risk_rating: str
    platform: str


@dataclasses.dataclass
class KBEntry:
    description: str
    recommendation: str
    meta: str


def _ask_the_wizard(
    prompts: list[dict[str, str]], temperature: float = 0.0, max_tokens: int = 3200
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
def generate_kb(vulnerability_name: str) -> KBEntry:
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
    wizard_answer = _ask_the_wizard(prompts=prompts)
    response = json.loads(wizard_answer.choices[0].message["content"])
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
    recommendation_buffer.write(f"{recommendation_data}\n\n")
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
    kbentry = KBEntry(description_md, recommendation_md, meta)

    return kbentry


def main() -> None:
    with open("vulnerabilities.csv", "r") as file:
        reader = dataclass_csv.DataclassReader(file, Vulnerability)
        vulnerabilities = list(reader)

    for vulnerability in vulnerabilities:
        kbentry = generate_kb(vulnerability.name)
        print(kbentry)  # TODO (BlueSquare1): Validate path and output to files


if __name__ == "__main__":
    main()
