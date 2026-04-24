from app.services.file_service.github_links import extract_github_links_from_text


def extract_links_from_txt_bytes(file_bytes: bytes) -> list[str]:
    text = file_bytes.decode("utf-8", errors="ignore")
    return sorted(extract_github_links_from_text(text))