from core.config import Settings


def test_settings_defaults() -> None:
    settings = Settings(OPENAI_API_KEY="test-key")
    assert settings.openai_model == "gpt-4.1"
    assert settings.openai_embedding_model == "text-embedding-3-small"
