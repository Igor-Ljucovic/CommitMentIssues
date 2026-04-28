from app.analyzers.general.average_commit_size_analyzer.average_commit_size_constants import (
    AVERAGE_COMMIT_SIZE_METRIC_KEY,
    BRANCH_NAME,
    TOTAL_ADDITIONS,
    TOTAL_DELETIONS,
    COMMIT_SIZE_SAMPLES,
    SAMPLED_COMMIT_NODES
)
from app.analyzers.general.average_commit_size_analyzer.average_commit_size_fetch import (
    fetch_average_commit_size,
)


async def average_commit_size_calculate(
    owner: str,
    repository_name: str,
) -> dict:
    result = await fetch_average_commit_size(
        owner=owner,
        repository_name=repository_name,
    )

    sampled_commit_nodes = result[SAMPLED_COMMIT_NODES]
    
    total_additions = sum(
        commit.get("additions") or 0
        for commit in sampled_commit_nodes
    )

    total_deletions = sum(
        commit.get("deletions") or 0
        for commit in sampled_commit_nodes
    )
    
    sampled_commits_count = len(sampled_commit_nodes)
    
    average_commit_size = (
        (total_additions + total_deletions) / sampled_commits_count
        if sampled_commits_count > 0
        else 0
    )

    commit_size_samples = [
        {
            "message": commit.get("messageHeadline"),
            "additions": commit.get("additions") or 0,
            "deletions": commit.get("deletions") or 0,
        }
        for commit in sampled_commit_nodes
    ]

    return {
        "owner": result["owner"],
        "repository_name": result["repository_name"],
        BRANCH_NAME: result[BRANCH_NAME],
        AVERAGE_COMMIT_SIZE_METRIC_KEY: average_commit_size,
        TOTAL_ADDITIONS: total_additions,
        TOTAL_DELETIONS: total_deletions,
        COMMIT_SIZE_SAMPLES: commit_size_samples,
    }