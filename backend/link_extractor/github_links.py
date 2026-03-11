import re
from urllib.parse import urlparse


GITHUB_URL_PATTERN = re.compile(
    r"https?://(?:www\.)?github\.com/"
    r"[A-Za-z0-9_.\-]+(?:/[A-Za-z0-9_.\-]+)*"
    r"(?:/[^\s)\]}>\"']*)?",
    re.IGNORECASE,
)


def clean_url(url: str) -> str:
    return url.rstrip(".,);]}>\"'")


def is_github_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        host = parsed.netloc.lower()
        return host in {"github.com", "www.github.com"}
    except Exception:
        return False


def extract_github_links_from_text(text: str) -> set[str]:
    return {
        cleaned_url
        for match in GITHUB_URL_PATTERN.findall(text)
        if is_github_url(cleaned_url := clean_url(match))
    }