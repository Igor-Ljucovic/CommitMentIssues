from app.analyzers.code_and_repository_quality.estimated_commit_naming_quality_analyzer.estimated_commit_naming_quality_constants import (
    COMMIT_HISTORY_PAGE_SIZE,
)


ESTIMATED_COMMIT_NAMING_QUALITY_GRAPHQL_QUERY = f"""
query GetRepositoryCommitHistory($owner: String!, $name: String!, $cursor: String) {{
  repository(owner: $owner, name: $name) {{
    name
    owner {{
      login
    }}
    defaultBranchRef {{
      name
      target {{
        ... on Commit {{
          history(first: {COMMIT_HISTORY_PAGE_SIZE}, after: $cursor) {{
            nodes {{
              messageHeadline
            }}
            pageInfo {{
              hasNextPage
              endCursor
            }}
          }}
        }}
      }}
    }}
  }}
}}
""".strip()