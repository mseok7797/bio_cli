from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str = Field(..., alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4.1", alias="OPENAI_MODEL")
    openai_embedding_model: str = Field(
        default="text-embedding-3-small",
        alias="OPENAI_EMBEDDING_MODEL",
    )
    openai_temperature: float = Field(default=0, alias="OPENAI_TEMPERATURE")
    openai_max_tokens: int = Field(default=900, alias="OPENAI_MAX_TOKENS")
    vector_db_path: str = Field(default="./data/vectorstore", alias="VECTOR_DB_PATH")
    pdf_data_path: str = Field(default="./data/samples", alias="PDF_DATA_PATH")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        populate_by_name=True,
        extra="ignore",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
