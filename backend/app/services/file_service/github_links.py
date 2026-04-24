import re
from urllib.parse import urlparse


GITHUB_URL_PATTERN = re.compile(
    r"https?://(?:www\.)?github\.com/[^\s)\]}>\"']+",
    re.IGNORECASE,
)

GITHUB_REPO_URL_PATTERN = re.compile(
    r"^https?://(?:www\.)?github\.com/"
    r"[A-Za-z0-9_.\-]+/[A-Za-z0-9_.\-]+"
    r"(?:\.git)?/?$",
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


def is_github_repo_url(url: str) -> bool:
    return bool(GITHUB_REPO_URL_PATTERN.match(url))


def normalize_github_repo_url(url: str) -> str:
    cleaned_url = clean_url(url)

    if cleaned_url.endswith("/"):
        cleaned_url = cleaned_url[:-1]

    if cleaned_url.lower().endswith(".git"):
        cleaned_url = cleaned_url[:-4]

    return cleaned_url


def extract_github_links_from_text(text: str) -> set[str]:
    links: set[str] = set()

    for match in GITHUB_URL_PATTERN.findall(text):
        cleaned_url = clean_url(match)

        if not is_github_url(cleaned_url):
            continue

        normalized_url = normalize_github_repo_url(cleaned_url)

        if is_github_repo_url(normalized_url):
            links.add(normalized_url)

    return links