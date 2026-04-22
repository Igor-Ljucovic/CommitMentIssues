TOTAL_FORKS_GRAPHQL_QUERY = """
query GetRepositoryForkCount($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) {
    name
    owner {
      login
    }
    forkCount
  }
}
""".strip()