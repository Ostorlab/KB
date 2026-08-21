"""Module responsible for interacting with the LLM API to generate KB entries."""

import dataclasses
import enum
import json
import logging
import os
import pathlib
import re
from typing import Any

import click
import tenacity
from openai import OpenAI
from openai.types import chat

DEMO_LANGS = ["Flutter", "Swift", "Kotlin"]

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

MODEL_NAME = "gpt-3.5-turbo"
FIREWORKS_MODEL_NAME = "accounts/fireworks/models/llama-v3p3-70b-instruct"
FIREWORKS_BASE_URL = "https://api.fireworks.ai/inference/v1"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


class LLMProvider(enum.Enum):
    """LLM inference provider used to generate the KB entries."""

    OPENROUTER = "openrouter"
    FIREWORKS = "fireworks"


DESCRIPTION_TEMPLATE = """
# %%VULNERABILITY_NAME%%

%%VULNERABILITY_DESCRIPTION%%

### Examples

#### Dart

```dart
%%FLUTTER_CODE%%
```

#### Swift

```swift
%%SWIFT_CODE%%
```

#### Kotlin

```kotlin
%%KOTLIN_CODE%%
```
"""

RECOMMENDATION_TEMPLATE = """
# %%VULNERABILITY_NAME%%

%%RECOMMENDATION%%

# Code Examples:

### Dart

```dart
%%FLUTTER_CODE%%
```

### Swift

```swift
%%SWIFT_CODE%%
```

### Kotlin

```kotlin
%%KOTLIN_CODE%%
```
"""

META_TEMPLATE = """
{
   "risk_rating":"[hardening/info/low/medium/high]",
   "short_description":"[short description of the vulnerability]",
   "references":{
      "Vulnerability (SOURCE)":"[SOURCE LINK]",
      ...
   },
   "title":"[Vulnerability title]",
   "privacy_issue":[true/false],
   "security_issue":[true/false],
   "categories":{
       "OWASP_MASVS_L1":[
         "MSTG reference" 
      ],
      "OWASP_MASVS_L2":[
         "MSTG reference"
      ]
   }
}
"""

PATTERN = "```(.*)```"


class RiskRating(enum.Enum):
    """RiskRating dataclass"""

    INFO = "INFO"
    HARDENING = "HARDENING"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


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


def dump_kb(kbentry: KBEntry) -> None:
    """Dump KB entry into files.

    Args:
        kbentry: Knowledge entry object.
    Returns:

    """
    path_prefix = pathlib.Path(
        PLATFORM_TO_PATH[kbentry.vulnerability.platform.value],
        f"_{kbentry.vulnerability.risk_rating.value}",
    )

    logger.info("KB generated successfully, path is %s", path_prefix)

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


def _ask_gpt(
    prompts: list[chat.ChatCompletionMessageParam],
    temperature: float = 0.0,
    max_tokens: int = 3200,
    provider: LLMProvider = LLMProvider.OPENROUTER,
) -> Any:
    """Send a prompt to the configured LLM provider using the OpenAI client."""
    if provider == LLMProvider.FIREWORKS:
        api_key = os.getenv("FIREWORKS_API_KEY")
        if api_key is None:
            raise ValueError("FIREWORKS_API_KEY environment variable is not set")
        client = OpenAI(
            api_key=api_key,
            base_url=FIREWORKS_BASE_URL,
        )
        model_name = FIREWORKS_MODEL_NAME
    else:
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key is None:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        client = OpenAI(
            api_key=api_key,
            base_url=OPENROUTER_BASE_URL,
        )
        model_name = MODEL_NAME

    return client.chat.completions.create(
        model=model_name,
        temperature=temperature,
        max_tokens=max_tokens,
        messages=prompts,
    )


@tenacity.retry(
    stop=tenacity.stop_after_attempt(3),
    wait=tenacity.wait_fixed(2),
    retry=tenacity.retry_if_exception_type(),
)
def generate_kb(
    vulnerability: Vulnerability, provider: LLMProvider = LLMProvider.OPENROUTER
) -> KBEntry:
    """Send a prompt to the LLM API and generate KB.

    Args:
        vulnerability: a vulnerability object
        provider: the LLM inference provider used to generate the KB entry
    Returns:
        KB entry

    """
    description_md = DESCRIPTION_TEMPLATE.replace(
        "%%VULNERABILITY_NAME%%", vulnerability.name.title()
    )
    prompt_message = (
        f"Vulnerability description for {vulnerability.name}, reply as one short paragraph without "
        f"mitigation details "
    )
    prompts: list[chat.ChatCompletionMessageParam] = [
        chat.ChatCompletionUserMessageParam(
            role="user",
            content=prompt_message,
        ),
    ]
    gpt_response = _ask_gpt(prompts=prompts, provider=provider)
    content = gpt_response.choices[0].message.content
    description_md = description_md.replace("%%VULNERABILITY_DESCRIPTION%%", content)

    recommendation_md = RECOMMENDATION_TEMPLATE.replace(
        "%%VULNERABILITY_NAME%%", vulnerability.name.title()
    )
    prompt_message = f"Vulnerability mitigation for {vulnerability.name}, reply as one short paragraph"
    prompts = [
        chat.ChatCompletionUserMessageParam(
            role="user",
            content=prompt_message,
        ),
    ]
    gpt_response = _ask_gpt(prompts=prompts, provider=provider)
    content = gpt_response.choices[0].message.content
    recommendation_md = recommendation_md.replace("%%RECOMMENDATION%%", content)

    for language in DEMO_LANGS:
        prompt_message = (
            f"Demo {language} application that is vulnerable to {vulnerability.name}, "
            "vulnerability has to depend on user input, "
            "application code has to include imports and main function"
            "your response need to consist of the code alone without any extra text"
        )
        prompts = [
            chat.ChatCompletionSystemMessageParam(
                role="system",
                content="act as a code generator, only reply with code, nothing else",
            ),
            chat.ChatCompletionUserMessageParam(
                role="user",
                content=prompt_message,
            ),
        ]
        gpt_response = _ask_gpt(prompts=prompts, provider=provider)
        content = gpt_response.choices[0].message.content
        match = re.search(PATTERN, content, re.DOTALL | re.MULTILINE)
        code = match.group(1).strip() if match else "[TODO]"
        description_md = description_md.replace(f"%%{language.upper()}_CODE%%", code)

        prompt_message = (
            f"The {language} code below is vulnerable to {vulnerability.name}, generate a patched version of it:"
            f"{content}"
        )
        prompts = [
            chat.ChatCompletionSystemMessageParam(
                role="system",
                content="act as a code generator, only reply with code, nothing else",
            ),
            chat.ChatCompletionUserMessageParam(
                role="user",
                content=prompt_message,
            ),
        ]
        gpt_response = _ask_gpt(prompts=prompts, provider=provider)
        content = gpt_response.choices[0].message.content
        match = re.search(PATTERN, content, re.DOTALL | re.MULTILINE)
        code = match.group(1).strip() if match else "[TODO]"
        recommendation_md = recommendation_md.replace(
            f"%%{language.upper()}_CODE%%", code
        )

    prompt_message = (
        f"Generate a metadata for {vulnerability.name} vulnerability, use the following template: "
        f"{META_TEMPLATE}"
    )
    prompts = [
        chat.ChatCompletionSystemMessageParam(
            role="system",
            content="act as a json metadata generator, only reply with json, nothing else",
        ),
        chat.ChatCompletionUserMessageParam(
            role="user",
            content=prompt_message,
        ),
    ]
    gpt_response = _ask_gpt(prompts=prompts, provider=provider)
    content = gpt_response.choices[0].message.content
    meta = json.loads(content)

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
@click.option(
    "--provider",
    help="LLM inference provider",
    type=click.Choice(
        [provider.value for provider in LLMProvider], case_sensitive=False
    ),
    default=LLMProvider.OPENROUTER.value,
    show_default=True,
)
def main(name: str, risk: str, platform: str, provider: str) -> None:
    """
    Entry point of the program.

    This function executes the main logic of the program, including initialization,
    user interactions, and finalization steps. It serves as the starting point for
    running the application.

    Args:
        name: vulnerability name
        risk: vulnerability risk rating
        platform: vulnerability target platform
        provider: LLM inference provider
    Returns:

    """
    vulnerability = Vulnerability(name, RiskRating(risk), Platform(platform))
    kbentry = generate_kb(vulnerability, LLMProvider(provider))
    dump_kb(kbentry)


if __name__ == "__main__":
    main()
