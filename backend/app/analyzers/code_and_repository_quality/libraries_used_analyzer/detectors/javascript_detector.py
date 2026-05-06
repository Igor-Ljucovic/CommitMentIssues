import json

from tree_sitter import Language, Parser
import tree_sitter_javascript as tsjavascript

from app.analyzers.code_and_repository_quality.libraries_used_analyzer.detectors.utils import (
    walk_nodes,
    get_node_text,
)

_NODE_STDLIB: frozenset[str] = frozenset({
    "assert", "buffer", "child_process", "cluster", "console",
    "crypto", "dgram", "dns", "domain", "events", "fs", "http",
    "http2", "https", "inspector", "module", "net", "os", "path",
    "perf_hooks", "process", "punycode", "querystring", "readline",
    "repl", "stream", "string_decoder", "timers", "tls", "tty",
    "url", "util", "v8", "vm", "worker_threads", "zlib",
})

_parser: Parser | None = None


def get_js_declared_packages_from_content(
    package_json_contents: list[str],
) -> frozenset[str]:
    declared: set[str] = set()
    for content in package_json_contents:
        declared.update(_parse_package_json(content))
    return frozenset(declared)


def parse_javascript_imports(source_code: str, js_declared: frozenset[str]) -> set[str]:
    tree = _get_parser().parse(source_code.encode("utf-8"))
    results: set[str] = set()
    for node in walk_nodes(tree.root_node, {"import_statement", "call_expression"}):
        if node.type == "import_statement":
            for child in node.children:
                if child.type == "string":
                    pkg = _pkg_from_string_node(child, js_declared)
                    if pkg:
                        results.add(pkg)
        elif node.type == "call_expression":
            fn_node = None
            args_node = None
            for child in node.children:
                if child.type == "identifier":
                    fn_node = child
                elif child.type == "arguments":
                    args_node = child
            if fn_node and fn_node.text == b"require" and args_node:
                for child in args_node.children:
                    if child.type == "string":
                        pkg = _pkg_from_string_node(child, js_declared)
                        if pkg:
                            results.add(pkg)
    return results


def _get_parser() -> Parser:
    global _parser
    if _parser is None:
        raw = tsjavascript.language()
        lang = raw if isinstance(raw, Language) else Language(raw)
        _parser = Parser(lang)
    return _parser


def _parse_package_json(content: str) -> set[str]:
    packages: set[str] = set()
    try:
        data = json.loads(content)
    except (json.JSONDecodeError, ValueError):
        return packages
    for key in ("dependencies", "devDependencies", "peerDependencies"):
        for name in data.get(key, {}).keys():
            if name:
                packages.add(name)
    return packages


def _pkg_from_string_node(string_node, js_declared: frozenset[str]) -> str | None:
    for sub in string_node.children:
        if sub.type == "string_fragment":
            pkg = _extract_package_name(get_node_text(sub))
            if pkg and pkg not in _NODE_STDLIB and _keep(pkg, js_declared):
                return pkg
    return None


def _extract_package_name(raw: str) -> str:
    text = raw.removeprefix("node:")
    if text.startswith("./") or text.startswith("../"):
        return ""
    # Skip path aliases like "@/components" (no scope name, just "@")
    # and invalid bare scopes like "@env" (missing the required "/name" part)
    if text.startswith("@"):
        parts = text.split("/")
        if parts[0] == "@" or len(parts) < 2:
            return ""
        return "/".join(parts[:2])
    return text.split("/")[0]


def _keep(pkg: str, js_declared: frozenset[str]) -> bool:
    if not js_declared:
        return True
    return pkg in js_declared
