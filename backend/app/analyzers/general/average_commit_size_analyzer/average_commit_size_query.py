AVERAGE_COMMIT_SIZE_GRAPHQL_QUERY = """
query GetRepositoryCommitSizes($owner: String!, $name: String!, $first: Int!, $after: String) {
  repository(owner: $owner, name: $name) {
    name
    owner {
      login
    }
    defaultBranchRef {
      name
      target {
        ... on Commit {
          history(first: $first, after: $after) {
            totalCount
            pageInfo {
              hasNextPage
              endCursor
            }
            nodes {
              messageHeadline
              additions
              deletions
            }
          }
        }
      }
    }
  }
}
""".strip()