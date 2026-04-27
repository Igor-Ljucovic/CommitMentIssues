LANGUAGES_USED_FILTERED_GRAPHQL_QUERY = """
query GetRepositoryLanguagesUsed($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) {
    name
    owner {
      login
    }
    languages(first: 100, orderBy: {field: SIZE, direction: DESC}) {
      totalSize
      edges {
        size
        node {
          name
        }
      }
    }
  }
}
""".strip()