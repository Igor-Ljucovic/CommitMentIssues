from datetime import datetime


def calculate_average_commits_per_month(
    total_commits: int,
    first_commit_date: str,
    last_commit_date: str,
) -> float:

    first_date = datetime.strptime(first_commit_date, "%Y-%m-%d")
    last_date = datetime.strptime(last_commit_date, "%Y-%m-%d")

    days_between = (last_date - first_date).days

    if days_between <= 0:
        # all commits in 1 month
        return float(total_commits)  

    months_between = days_between / (365.25 / 12)

    if months_between == 0:
        return float(total_commits)

    return total_commits / months_between