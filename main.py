from __future__ import annotations

from pathlib import Path

import typer

from agent.graph import run_agent
from core.config import Settings, get_settings
from core.rag import ingest_documents, preview_retrieval

app = typer.Typer(help="Nutrition and exercise physiology CLI agent.")


def load_settings() -> Settings:
    try:
        return get_settings()
    except Exception as exc:  # pragma: no cover - surfaced to CLI
        raise typer.BadParameter(str(exc)) from exc


@app.command()
def doctor() -> None:
    """Validate the local environment and expected data paths."""
    settings = load_settings()
    pdf_dir = Path(settings.pdf_data_path)
    vector_dir = Path(settings.vector_db_path)

    typer.echo(f"OPENAI_MODEL={settings.openai_model}")
    typer.echo(f"OPENAI_EMBEDDING_MODEL={settings.openai_embedding_model}")
    typer.echo(f"PDF_DATA_PATH={pdf_dir.resolve()}")
    typer.echo(f"VECTOR_DB_PATH={vector_dir.resolve()}")

    if not settings.openai_api_key:
        raise typer.BadParameter("OPENAI_API_KEY is not set.")

    if not pdf_dir.exists():
        typer.echo("PDF data directory does not exist yet.")
    else:
        pdf_count = len(list(pdf_dir.rglob("*.pdf")))
        typer.echo(f"PDF files found: {pdf_count}")

    typer.echo("Environment looks ready.")


@app.command()
def ingest(rebuild: bool = typer.Option(True, help="Rebuild the vector store from PDFs.")) -> None:
    """Index PDFs into the local FAISS vector store."""
    settings = load_settings()
    indexed = ingest_documents(settings=settings, rebuild=rebuild)
    typer.echo(f"Indexed chunks: {indexed}")


@app.command()
def query(question: str) -> None:
    """Show retrieval results only."""
    settings = load_settings()
    docs = preview_retrieval(question=question, settings=settings)

    if not docs:
        typer.echo("검색 결과가 없습니다. 먼저 PDF를 추가하고 `bio ingest`를 실행하세요.")
        return

    for idx, doc in enumerate(docs, start=1):
        source = doc.metadata.get("source", "unknown")
        page = doc.metadata.get("page", "n/a")
        typer.echo(f"[{idx}] source={source} page={page}")
        typer.echo(doc.page_content[:400].strip())
        typer.echo("")


@app.command()
def ask(question: str) -> None:
    """Run the full agent workflow."""
    settings = load_settings()
    result = run_agent(question=question, settings=settings)
    typer.echo(result["final_answer"])


if __name__ == "__main__":
    app()
