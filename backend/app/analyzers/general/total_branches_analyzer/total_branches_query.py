TOTAL_BRANCHES_GRAPHQL_QUERY = """
query GetRepositoryBranchCount($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) {
    name
    owner {
      login
    }
    refs(refPrefix: "refs/heads/", first: 1) {
      totalCount
    }
  }
}
""".strip()