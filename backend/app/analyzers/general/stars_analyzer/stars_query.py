TOTAL_STARS_GRAPHQL_QUERY = """
query GetRepositoryStarCount($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) {
    repository_name: name
    repository_owner: owner {
      login
    }
    stars: stargazerCount
  }
}
""".strip()