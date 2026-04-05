PULL_REQUEST_ACCEPTANCE_RATE_GRAPHQL_QUERY = """
query GetPullRequestAcceptanceRate($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) {
    name
    owner {
      login
    }
    mergedPullRequests: pullRequests(states: [MERGED], first: 1) {
      totalCount
    }
    closedPullRequests: pullRequests(states: [CLOSED], first: 1) {
      totalCount
    }
  }
}
""".strip()