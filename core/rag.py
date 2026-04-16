from __future__ import annotations

from pathlib import Path
from shutil import rmtree

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from core.config import Settings
from core.llm import get_embeddings


def load_documents(pdf_dir: str) -> list[Document]:
    base = Path(pdf_dir)
    if not base.exists():
        return []

    docs: list[Document] = []
    for path in sorted(base.rglob("*.pdf")):
        loader = PyPDFLoader(str(path))
        docs.extend(loader.load())
    return docs


def split_documents(documents: list[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=150,
        separators=["\n\n", "\n", ". ", " "],
    )
    return splitter.split_documents(documents)


def ingest_documents(settings: Settings, rebuild: bool = True) -> int:
    source_docs = load_documents(settings.pdf_data_path)
    if not source_docs:
        return 0

    chunks = split_documents(source_docs)
    db_path = Path(settings.vector_db_path)
    if rebuild and db_path.exists():
        rmtree(db_path)

    embeddings = get_embeddings(settings)
    vectorstore = FAISS.from_documents(chunks, embeddings)
    db_path.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(db_path))
    return len(chunks)


def get_vector_store(settings: Settings) -> FAISS | None:
    db_path = Path(settings.vector_db_path)
    if not db_path.exists():
        return None

    embeddings = get_embeddings(settings)
    return FAISS.load_local(
        str(db_path),
        embeddings,
        allow_dangerous_deserialization=True,
    )


def retrieve_documents(question: str, settings: Settings, limit: int = 4) -> list[Document]:
    vectorstore = get_vector_store(settings)
    if vectorstore is None:
        return []
    return vectorstore.similarity_search(question, k=limit)


def preview_retrieval(question: str, settings: Settings, limit: int = 4) -> list[Document]:
    return retrieve_documents(question=question, settings=settings, limit=limit)
