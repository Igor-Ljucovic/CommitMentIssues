GITHUB_WIKI_ENABLED_QUERY = """
query GetGitHubWikiEnabled($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) {
    name
    owner {
      login
    }
    hasWikiEnabled
  }
}
""".strip()