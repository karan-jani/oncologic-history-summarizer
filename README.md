# Zero-shot Thoracic Oncologic History Generation for Radiologists using Retrieval-Augmented Large Language Model Pipeline

This repository is the base implementation of a structured oncologic history summarization tool to aid radiologists when interpreting follow-up studies on cancer patients. 

This repository exposes:
- object schemas used for structured oncologic summaries
- DSPy signatures used to generate those summaries
- basic CLI that reads dated note context from JSON and writes structured output to JSON

## Quickstart

1. Install dependencies:

```bash
uv sync
```

2. Copy `.env.example` to `.env` and fill in your Azure OpenAI settings:

```bash
cp .env.example .env
```

Then edit `.env` so it contains your Azure OpenAI API key, endpoint, and deployment name.

3. Run the example:

```bash
uv run python cli.py \
  --input examples/synthetic_context.json \
  --output output/summary.json
```

This writes `output/summary.json` with a top-level `structured_summary` key.

If you are using an Azure GPT-4.1 deployment, you can optionally apply the tested GPT-4.1 temperature setting:

```bash
uv run python cli.py \
  --input examples/mock_notes.json \
  --output output/summary.json \
  --gpt41
```

## Input Format

The input file must be JSON and must contain a list of note objects with `date` and `context` keys:

```json
[
  {
    "date": "2026-01-14",
    "context": "Clinical note or report text"
  }
]
```

The bundled examples/ directory contains synthetic data with the appropriate structure.

## Repository Layout

- `schemas.py`: Pydantic models for structured output
- `dspy_modules.py`: DSPy signatures and modules
- `cli.py`: command-line entrypoint
- `examples/mock_notes.json`: mock dated oncology notes for testing

## Notes
- The CLI expects your Azure credentials to be present in `.env`.
- The main workflow is file-based: input JSON in, structured summary JSON out.
- The DSPy signature is the same for all runs. The CLI always wraps the generated list into the same `structured_summary.onc_summary` output shape.
- `--gpt41` does not change the parser or schema. It only applies `temperature=0.2`, which was the tested setting for Azure GPT-4.1 deployments. This does not apply to reasoning models (GPT-5, etc.), which have a fixed temperature of 1.0. 
