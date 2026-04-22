ESTIMATED_COMMIT_NAMING_QUALITY_METRIC_KEY = "estimated_commit_naming_quality"
ESTIMATED_COMMIT_NAMING_QUALITY_METRIC_NAME = "Estimated Commit Naming Quality"
ESTIMATED_COMMIT_NAMING_QUALITY_CATEGORY_NAME = "Code & Repository Quality"
ESTIMATED_COMMIT_NAMING_QUALITY_SUBCATEGORY_NAME = "Estimated Commit Naming Quality"

BRANCH_NAME = "branch_name"
COMMIT_MESSAGES = "commit_messages"

ESTIMATED_COMMIT_NAMING_QUALITY_SAMPLE_SIZE = 40
ESTIMATED_COMMIT_NAMING_QUALITY_SAMPLE_SEED = 69
COMMIT_HISTORY_PAGE_SIZE = 100

CONSISTENCY_MAX_SCORE = 2.5
LENGTH_MAX_SCORE = 2.5
GOOD_PRACTICE_MAX_SCORE = 2.5
BAD_PRACTICE_MAX_SCORE = 2.5

# 1 bad practice word every 5 commits = 0 points
# (and linear in between)
PER_BAD_PRACTICE_OCCURRENCE_PENALTY = (
    BAD_PRACTICE_MAX_SCORE
    / (ESTIMATED_COMMIT_NAMING_QUALITY_SAMPLE_SIZE / 5)
)

# 1 inconsistency every 10 commits = 0 points
# (and linear in between)
PER_INCONSISTENT_COMMIT_PENALTY = (
    CONSISTENCY_MAX_SCORE
    / (ESTIMATED_COMMIT_NAMING_QUALITY_SAMPLE_SIZE / 10)
)

ACTION_FAMILIES: list[set[str]] = [
    {"add"},
    {"remove", "delete"},
    {"refactor"},
    {"fix"},
    {"update"},
    {"rename"},
    {"implement"},
    {"create"},
    {"improve"},
    {"cleanup", "clean"},
    {"revert"},
    {"move"},
    {"extract"},
    {"optimize", "optimise"},
    {"test"},
    {"docs", "document"},
    {"chore"},
    {"feat", "feature"},
    {"bugfix"},
]

GOOD_PRACTICE_TERMS: set[str] = {
    # DevOps / infrastructure
    "docker",
    "container",
    "kubernetes",
    "k8s",
    "nginx",
    "apache",
    "ci",
    "cd",
    "pipeline",
    "workflow",
    "deployment",
    "deploy",
    "env",
    "environment",
    "infrastructure",

    # Security
    "oauth",
    "encryption",
    "hash",
    "bcrypt",
    "security",
    "permission",
    "role",
    "access",
    "csrf",
    "cors",
    "xss",

    # Testing
    "integration",
    "unittest",
    "e2e",
    "mock",
    "fixture",
    "benchmark",

    # Frontend ecosystem
    "react",
    "vue",
    "angular",
    "typescript",
    "javascript",
    "css",
    "html",
    "tailwind",
    "redux",
    "zustand",

    # Backend ecosystem
    "python",
    "csharp",
    "dotnet",
    "aspnet",
    "fastapi",
    "flask",
    "django",
    "laravel",
    "spring",
    "java",

    # Data / AI / analytics
    "ml",
    "ai",
    "dataset",
    "training",
    "inference",
    "prediction",
    "classifier",
    "embedding",
    "vector",
    "transformer",
    "evaluation",
    "accuracy",
    "ranking",

    # Git / repo workflow
    "merge",
    "rebase",
    "commitlint",
    "changelog",
    "release",
    "version",

    # Performance
    "performance",
    "optimization",
    "memory",
    "cpu",
    "latency",
    "throughput",
    "parallel",
    "concurrency",

    # Architecture / patterns
    "singleton",
    "factory",
    "repositorypattern",
    "dependencyinjection",
    "di",
    "adapter",
    "facade",
    "strategy",

    # General
    "page",
    "api",
    "repo",
    "repository",
    "backend",
    "frontend",
    "ui",
    "controller",
    "service",
    "client",
    "server",
    "endpoint",
    "route",
    "auth",
    "login",
    "database",
    "db",
    "sql",
    "migration",
    "schema",
    "model",
    "dto",
    "entity",
    "component",
    "cache",
    "config",
    "metric",
    "analysis",
    "upload",
    "issue",
    "bug",
    "query",
    "response",
    "request",
    "test",
    "tests",
    "readme",
}

BAD_PRACTICE_TERMS: set[str] = {
    "thing",
    "things",
    "stuff",
    "misc",
    "tmp",
    "temp",
    "wip",
    "whatever",
    "random",
    "fixes",
    "updates",
    "some",
    "something",
}