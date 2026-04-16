from __future__ import annotations

from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from core.config import Settings


def get_chat_model(settings: Settings) -> ChatOpenAI:
    return ChatOpenAI(
        api_key=settings.openai_api_key,
        model=settings.openai_model,
        temperature=settings.openai_temperature,
        max_tokens=settings.openai_max_tokens,
        use_responses_api=True,
    )


def get_embeddings(settings: Settings) -> OpenAIEmbeddings:
    return OpenAIEmbeddings(
        api_key=settings.openai_api_key,
        model=settings.openai_embedding_model,
    )
