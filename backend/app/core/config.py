from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    # some values have default values because they are not secrets
    # and because, hypothetically, if this app was being developed in a team,
    # all of the developers would use the same default values
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    FRONTEND_ORIGIN: str

    GITHUB_TOKEN: str
    GITHUB_GRAPHQL_URL: str = "https://api.github.com/graphql"
    GITHUB_REST_API_BASE_URL: str = "https://api.github.com"
    GITHUB_REQUEST_TIMEOUT_SECONDS: int = 30
    
    OPENAI_API_BASE_URL: str = "https://api.openai.com/v1"
    OPENAI_API_KEY: str = ""
    OPENAI_REQUEST_TIMEOUT_SECONDS: int = 60

    LOCAL_LLM_PROVIDER: str = "ollama"
    LOCAL_LLM_BASE_URL: str = "http://localhost:11434"
    LOCAL_LLM_MODEL: str = "qwen2.5-coder:7b"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore",
    )


settings = Settings()