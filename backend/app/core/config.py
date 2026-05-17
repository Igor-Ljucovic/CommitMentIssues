from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent.parent
GITHUB_REPOSITORIES_DIRECTORY = BASE_DIR / "uploads" / "github_repositories"


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
    GITHUB_MAX_CONCURRENT_TARBALL_DOWNLOADS: int = 4
    GITHUB_MAX_REPOSITORY_SIZE_KB: int = 500000
    
    OPENAI_API_BASE_URL: str = "https://api.openai.com/v1"
    OPENAI_API_KEY: str = ""
    OPENAI_REQUEST_TIMEOUT_SECONDS: int = 60
    OPENAI_MODEL_GPT41MINI: str = "gpt-4.1-mini"

    LOCAL_LLM_PROVIDER: str = "ollama"
    LOCAL_LLM_BASE_URL: str = "http://localhost:11434"
    LOCAL_LLM_MODEL_QWEN25CODER7B: str = "qwen2.5-coder:7b"

    REDIS_URL: str = "redis://localhost:6379"
    REDIS_CACHE_SESSION_TTL_SECONDS: int = 1800  # 30 minutes

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore",
    )


settings = Settings()