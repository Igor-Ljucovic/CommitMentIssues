LAST_COMMIT_DATE_GRAPHQL_QUERY = """
query GetLastCommitDate($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) {
    name
    owner {
      login
    }
    defaultBranchRef {
      name
      target {
        ... on Commit {
          history(first: 1) {
            nodes {
              committedDate
            }
          }
        }
      }
    }
  }
}
""".strip()