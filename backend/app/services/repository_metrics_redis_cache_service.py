import json

import redis.asyncio as aioredis

from app.core.config import settings
from app.schemas.analysis_response_schemas import RepositoryMetricResult

_client: aioredis.Redis | None = None


def _get_client() -> aioredis.Redis:
    global _client
    if _client is None:
        # decode_responses - return str instead of bytes, so we can directly json.loads without decoding
        _client = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
    return _client


def _repository_key(repo_url: str) -> str:
    # "https://github.com/User/Repo/" becomes "repository_metrics:https://github.com/user/repo"
    return f"repository_metrics:{repo_url.rstrip('/').lower()}"


async def get_cached_metrics(repo_url: str) -> list[RepositoryMetricResult] | None:
    try:
        raw = await _get_client().get(_repository_key(repo_url))
        if raw is None:
            return None
        return [RepositoryMetricResult.model_validate(m) for m in json.loads(raw)]
    except Exception:
        return None


async def cache_metrics(repo_url: str, metrics: list[RepositoryMetricResult]) -> None:
    try:
        payload = json.dumps([m.model_dump() for m in metrics])
        await _get_client().set(_repository_key(repo_url), payload, ex=settings.REDIS_CACHE_SESSION_TTL_SECONDS)
    except Exception:
        pass
