# bio-cli

`bio-cli` is a Typer-based CLI for nutrition and exercise physiology Q&A. It uses LangGraph for agent orchestration, OpenAI for generation and embeddings, and FAISS for local retrieval.

## Features

- OpenAI `gpt-4.1` as the default generation model
- OpenAI `text-embedding-3-small` for embeddings
- LangGraph workflow with planner, researcher, writer, and reviewer nodes
- Korean-first answers with a built-in safety disclaimer
- Local FAISS vector store for PDF-based retrieval

## Setup

### 1. Create a virtual environment and install dependencies

```bash
cd /path/to/bio-cli
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -e .
```

### 2. Copy `.env.example` to `.env`

```bash
cp .env.example .env
```

Then edit `.env` and set your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4.1
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_TEMPERATURE=0
OPENAI_MAX_TOKENS=900
VECTOR_DB_PATH=./data/vectorstore
PDF_DATA_PATH=./data/samples
```

### 3. Add text-based sample PDFs to `data/samples/`

You can place your own PDFs in `data/samples/`, or start with files named like:

```bash
data/samples/nutrition-basics.pdf
data/samples/exercise-physiology-overview.pdf
data/samples/sleep-recovery-guide.pdf
```

Use text-selectable PDFs first. Scanned PDFs often require OCR and may reduce early retrieval quality.

### 4. Validate the setup

```bash
bio doctor
```

### 5. Build the vector index

```bash
bio ingest
```

### 6. Test retrieval

```bash
bio query "단백질 섭취와 수면 회복의 기본 원칙"
```

### 7. Run the full agent workflow

```bash
bio ask "단백질 섭취와 수면 회복의 기본 원칙을 요약해줘"
```

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

## Example workflow

```bash
cd /path/to/bio-cli
source .venv/bin/activate
bio doctor
bio ingest
bio query "운동 후 단백질 섭취의 핵심 원칙은 무엇인가?"
bio ask "운동 후 단백질 섭취와 수면 회복의 관계를 설명해줘"
```

Expected flow:

1. `bio doctor` checks environment variables and sample PDFs.
2. `bio ingest` loads PDFs and builds the FAISS vector store.
3. `bio query` shows matching document chunks.
4. `bio ask` runs the planner, researcher, writer, and reviewer flow and returns a Korean answer.

## Safety policy

Every final answer includes a short reminder that the response is informational and not medical diagnosis or treatment advice.
