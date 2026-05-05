import asyncio
import base64

from app.services.github_rest_service import fetch_github_rest_resource


async def fetch_with_retry(endpoint: str, params: dict | None = None) -> dict:
    """Retry up to 3 times with exponential back-off for transient DNS/network errors."""
    last_exc: Exception = RuntimeError("Unknown error")
    for attempt in range(3):
        try:
            return await fetch_github_rest_resource(endpoint, params=params)
        except Exception as exc:
            last_exc = exc
            if attempt < 2:
                await asyncio.sleep(0.5 * (2 ** attempt))
    raise last_exc


async def fetch_blob_text(owner: str, repository_name: str, blob_sha: str) -> str | None:
    """Fetch a blob and return its decoded text, or None on failure."""
    try:
        blob_data = await fetch_github_rest_resource(
            f"/repos/{owner}/{repository_name}/git/blobs/{blob_sha}"
        )
        if blob_data.get("encoding") != "base64":
            return None
        file_bytes = base64.b64decode(
            blob_data.get("content", "").replace("\n", "")
        )
        if b"\x00" in file_bytes:
            return None
        try:
            return file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            try:
                return file_bytes.decode("utf-8-sig")
            except UnicodeDecodeError:
                return None
    except Exception:
        return None


def walk_nodes(root_node, target_types: set[str]):
    """Iterative DFS over a tree-sitter tree — yields nodes whose type is in target_types."""
    stack = [root_node]
    while stack:
        node = stack.pop()
        if node.type in target_types:
            yield node
        stack.extend(reversed(node.children))


def get_node_text(node) -> str:
    return node.text.decode("utf-8") if node.text else ""
