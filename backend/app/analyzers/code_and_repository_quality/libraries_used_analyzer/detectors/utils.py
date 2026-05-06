def walk_nodes(root_node, target_types: set[str]):
    """Iterative DFS over a tree-sitter tree - yields nodes whose type is in target_types."""
    stack = [root_node]
    while stack:
        node = stack.pop()
        if node.type in target_types:
            yield node
        stack.extend(reversed(node.children))


def get_node_text(node) -> str:
    return node.text.decode("utf-8") if node.text else ""
