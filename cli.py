from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import dspy
from dotenv import load_dotenv

from dspy_modules import OncSummaryList, RAGSummaryGeneration
from schemas import StructuredOncSummaries, SummaryContext


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a structured oncology summary from dated JSON note context."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to a JSON file containing a list of {date, context} note objects.",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Path to the JSON file that will receive the structured summary.",
    )
    parser.add_argument(
        "--gpt41",
        action="store_true",
        help="Apply the tested GPT-4.1 temperature setting of 0.2.",
    )
    return parser.parse_args()


def load_contexts(path: Path) -> list[SummaryContext]:
    message = "Input must be a JSON file containing date/context note objects. Please see examples/mock_notes.json."

    if path.suffix.lower() != ".json": 
        raise ValueError(message)

    try:
        raw_items = json.loads(path.read_text())
        return [SummaryContext.model_validate(item) for item in raw_items]
    except Exception as exc:
        raise ValueError(message) from exc


def main() -> None:
    load_dotenv()
    args = parse_args()
    input_path = Path(args.input).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()

    deployment = os.getenv("AZURE_DEPLOYMENT_NAME")
    api_key = os.getenv("AZURE_API_KEY")
    endpoint = os.getenv("AZURE_ENDPOINT")
    assert deployment and api_key and endpoint, (
        "Set AZURE_DEPLOYMENT_NAME, AZURE_API_KEY, and AZURE_ENDPOINT before running the CLI."
    )

    contexts = load_contexts(input_path)

    generate = dspy.ChainOfThought(RAGSummaryGeneration, response_format=OncSummaryList)
    lm_kwargs = {
        "model": f"azure/{deployment}",
        "api_key": api_key,
        "api_base": endpoint,
        "response_format": OncSummaryList,
    }
    if args.gpt41:
        lm_kwargs["temperature"] = 0.1
    lm = dspy.LM(**lm_kwargs)

    with dspy.context(lm=lm):
        generated = generate(context=contexts)

    summary = StructuredOncSummaries(onc_summary=generated.onc_summary.root)

    payload = {"structured_summary": summary.model_dump(mode="json")}
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"Wrote structured summary to {output_path}")


if __name__ == "__main__":
    main()
