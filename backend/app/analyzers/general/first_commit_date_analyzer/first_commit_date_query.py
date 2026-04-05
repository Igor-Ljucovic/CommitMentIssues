FIRST_COMMIT_DATE_GRAPHQL_QUERY = """
query GetFirstCommitDatePage($owner: String!, $name: String!, $cursor: String) {
  repository(owner: $owner, name: $name) {
    name
    owner {
      login
    }
    defaultBranchRef {
      name
      target {
        ... on Commit {
          history(first: 100, after: $cursor) {
            nodes {
              committedDate
            }
            pageInfo {
              hasNextPage
              endCursor
            }
          }
        }
      }
    }
  }
}
""".strip()