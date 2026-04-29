AVERAGE_COMMIT_SIZE_METRIC_KEY = "average_commit_size"
AVERAGE_COMMIT_SIZE_METRIC_NAME = "Average Commit Size"
AVERAGE_COMMIT_SIZE_CATEGORY_NAME = "General"
AVERAGE_COMMIT_SIZE_SUBCATEGORY_NAME = "Average Commit Size"

BRANCH_NAME = "branch_name"
# nodes are used temporarily in the fetch method to create
# COMMIT_SIZE_SAMPLES later
SAMPLED_COMMIT_NODES = "sampled_commit_nodes"
SAMPLED_COMMITS_COUNT = "sampled_commits_count"
TOTAL_ADDITIONS = "total_additions"
TOTAL_DELETIONS = "total_deletions"
# COMMIT_SIZE_SAMPLES have "message", "additions", deletions"
COMMIT_SIZE_SAMPLES = "commit_size_samples"

GITHUB_GRAPHQL_PAGE_SIZE_LIMIT = 100

# every 100 commits, a new API call needs to be called,
# the commits start from the first 100, then the next 100...
AVERAGE_COMMIT_SIZE_SAMPLE_SIZE = 300