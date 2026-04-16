from core.rag import split_documents
from langchain_core.documents import Document


def test_split_documents_returns_chunks() -> None:
    docs = [Document(page_content="단백질은 근육 합성에 필요하다. " * 120)]
    chunks = split_documents(docs)
    assert len(chunks) >= 2
