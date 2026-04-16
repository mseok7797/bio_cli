# bio-cli

`bio-cli` is a Typer-based CLI for nutrition and exercise physiology Q&A. It uses LangGraph for agent orchestration, OpenAI for generation and embeddings, and FAISS for local retrieval.

## Features

- OpenAI `gpt-4.1` as the default generation model
- OpenAI `text-embedding-3-small` for embeddings
- LangGraph workflow with planner, researcher, writer, and reviewer nodes
- Korean-first answers with a built-in safety disclaimer
- Local FAISS vector store for PDF-based retrieval

## Setup

1. Create a virtual environment and install dependencies.
2. Copy `.env.example` to `.env` and set `OPENAI_API_KEY`.
3. Add text-based sample PDFs to `data/samples/`.

## Commands

- `bio doctor`: validate environment and data directory
- `bio ingest`: load PDFs and build the FAISS index
- `bio query "질문"`: inspect retrieved chunks only
- `bio ask "질문"`: run the LangGraph workflow and return a Korean answer

## Sample PDFs

This scaffold assumes placeholder sample topics rather than bundled PDFs:

- `nutrition-basics.pdf`
- `exercise-physiology-overview.pdf`
- `sleep-recovery-guide.pdf`

Use text-selectable PDFs first. Scanned PDFs typically need OCR and will degrade early retrieval quality.

## Safety policy

Every final answer includes a short reminder that the response is informational and not medical diagnosis or treatment advice.

## Additional documents

- `docs/README_INTRO.md`: short intro text for README reuse
- `docs/PORTFOLIO_SUMMARY.md`: condensed portfolio summary
- `docs/PROJECT_REPORT_FULL.md`: full project report
- `docs/FLOW_AND_ARCHITECTURE.md`: flow and architecture guide with Mermaid diagrams
