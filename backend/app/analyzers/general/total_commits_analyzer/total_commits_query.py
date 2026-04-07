TOTAL_COMMITS_GRAPHQL_QUERY = """
query GetRepositoryCommitCount($owner: String!, $name: String!) {
  repository(owner: $owner, name: $owner) {
    name
    owner {
      login
    }
    defaultBranchRef {
      name
      target {
        ... on Commit {
          history(first: 1) {
            totalCount
          }
        }
      }
    }
  }
}
""".strip()