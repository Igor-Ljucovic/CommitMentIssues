from __future__ import annotations

import random
import re
from dataclasses import dataclass, field

from app.analyzers.code_and_repository_quality.estimated_commit_naming_quality_analyzer.estimated_commit_naming_quality_constants import (
    ACTION_FAMILIES,
    BAD_PRACTICE_TERMS,
    CONSISTENCY_MAX_SCORE,
    LENGTH_MAX_SCORE,
    GOOD_PRACTICE_MAX_SCORE,
    BAD_PRACTICE_MAX_SCORE,
    ESTIMATED_COMMIT_NAMING_QUALITY_SAMPLE_SEED,
    ESTIMATED_COMMIT_NAMING_QUALITY_SAMPLE_SIZE,
    GOOD_PRACTICE_TERMS,
    PER_BAD_PRACTICE_OCCURRENCE_PENALTY,
    PER_INCONSISTENT_COMMIT_PENALTY,
)


TOKEN_REGEX = re.compile(r"[A-Za-z0-9_+-]+")
LEADING_TOKEN_REGEX = re.compile(r"^\s*([A-Za-z][A-Za-z0-9_+-]*:?)(?:\s+|$)")


@dataclass(slots=True)
class CommitAnalysis:
    message: str
    length: int
    length_score_normalized: float
    leading_variant: str | None
    leading_family: str | None
    good_terms_found: list[str] = field(default_factory=list)
    bad_terms_found: list[str] = field(default_factory=list)
    counted_for_consistency: bool = False
    counted_for_good_terms: bool = False


@dataclass(slots=True)
class CommitNamingQualityBreakdown:
    sample_size: int
    sampled_commits: list[str]
    consistency_score: float
    length_score: float
    conventional_words_score: float
    bad_practice_score: float
    total_score: float
    commit_analyses: list[CommitAnalysis]


def calculate_estimated_commit_naming_quality(
    commit_messages: list[str],
) -> float:
    rating = calculate_estimated_commit_naming_quality_breakdown(
        commit_messages=commit_messages,
    ).total_score
    
    return round(rating * 0.1, 2)


def calculate_estimated_commit_naming_quality_breakdown(
    commit_messages: list[str],
    sample_size: int =  ESTIMATED_COMMIT_NAMING_QUALITY_SAMPLE_SIZE,
    seed: int | None = ESTIMATED_COMMIT_NAMING_QUALITY_SAMPLE_SEED,
) -> CommitNamingQualityBreakdown:
    sampled_commits = _sample_commits(
        commits=commit_messages,
        sample_size=sample_size,
        seed=seed,
    )
    analyses = _analyze_commits(sampled_commits)

    consistency_score = _score_consistency(analyses)
    length_score = _score_length(analyses)
    conventional_words_score = _score_good_technical_terms(analyses)
    bad_practice_score = _score_bad_practices(analyses)

    total_score = (
        consistency_score
        + length_score
        + conventional_words_score
        + bad_practice_score
    )
    MAX_TOTAL_SCORE = (
        CONSISTENCY_MAX_SCORE
        + LENGTH_MAX_SCORE
        + GOOD_PRACTICE_MAX_SCORE
        + BAD_PRACTICE_MAX_SCORE
    )
    total_score = max(0.0, min(MAX_TOTAL_SCORE, total_score))

    return CommitNamingQualityBreakdown(
        sample_size=len(sampled_commits),
        sampled_commits=sampled_commits,
        consistency_score=round(consistency_score, 4),
        length_score=round(length_score, 4),
        conventional_words_score=round(conventional_words_score, 4),
        bad_practice_score=round(bad_practice_score, 4),
        total_score=round(total_score, 4),
        commit_analyses=analyses,
    )


def _sample_commits(
    commits: list[str],
    sample_size: int,
    seed: int | None,
) -> list[str]:
    if sample_size <= 0:
        raise ValueError("sample_size must be greater than 0.")

    if not commits:
        return []

    actual_size = min(sample_size, len(commits))
    rng = random.Random(seed)
    return rng.sample(commits, actual_size)


def _tokenize(text: str) -> list[str]:
    return TOKEN_REGEX.findall(text.lower())


def _normalize_action_token(raw_token: str) -> str:
    return raw_token.rstrip(":").lower()


def _find_action_family(normalized_action: str) -> str | None:
    for family in ACTION_FAMILIES:
        if normalized_action in family:
            return sorted(family)[0]
    return None


def _extract_leading_variant(message: str) -> tuple[str | None, str | None]:
    match = LEADING_TOKEN_REGEX.match(message)
    if not match:
        return None, None

    raw_variant = match.group(1)
    normalized = _normalize_action_token(raw_variant)
    family = _find_action_family(normalized)

    if family is None:
        return None, None

    return raw_variant, family


def _length_score_normalized(length: int) -> float:
    if length <= 0:
        return 0.0

    if length < 20:
        return length / 20.0

    if 20 <= length <= 60:
        return 1.0

    if 60 < length < 100:
        return max(0.0, 1.0 - ((length - 50) / 50.0))

    return 0.0


def _normalize_compound_token(token: str) -> str:
    return re.sub(r"[_+-]", "", token.lower())


def _analyze_commits(sampled_commits: list[str]) -> list[CommitAnalysis]:
    analyses: list[CommitAnalysis] = []

    for commit in sampled_commits:
        tokens = _tokenize(commit)
        raw_variant, family = _extract_leading_variant(commit)

        good_terms = sorted(
            {
                token
                for token in tokens
                if _normalize_compound_token(token) in GOOD_PRACTICE_TERMS
            }
        )
        bad_terms = sorted(
            {token for token in tokens if token in BAD_PRACTICE_TERMS}
        )

        analyses.append(
            CommitAnalysis(
                message=commit,
                length=len(commit),
                length_score_normalized=_length_score_normalized(len(commit)),
                leading_variant=raw_variant,
                leading_family=family,
                good_terms_found=good_terms,
                bad_terms_found=bad_terms,
            )
        )

    return analyses


def _score_consistency(analyses: list[CommitAnalysis]) -> float:
    family_to_variant_counts: dict[str, dict[str, int]] = {}

    for analysis in analyses:
        if analysis.leading_family is None or analysis.leading_variant is None:
            continue

        family_counts = family_to_variant_counts.setdefault(
            analysis.leading_family,
            {},
        )
        family_counts[analysis.leading_variant] = (
            family_counts.get(analysis.leading_variant, 0) + 1
        )

    dominant_variants_by_family: dict[str, str] = {}
    inconsistent_commit_count = 0

    for family, variant_counts in family_to_variant_counts.items():
        dominant_variant = max(
            variant_counts.items(),
            key=lambda item: item[1],
        )[0]
        dominant_variants_by_family[family] = dominant_variant

    for analysis in analyses:
        if analysis.leading_family is None or analysis.leading_variant is None:
            continue

        is_consistent = (
            dominant_variants_by_family.get(analysis.leading_family)
            == analysis.leading_variant
        )

        if is_consistent:
            analysis.counted_for_consistency = True
        else:
            inconsistent_commit_count += 1

    score = CONSISTENCY_MAX_SCORE - (
        inconsistent_commit_count * PER_INCONSISTENT_COMMIT_PENALTY
    )

    return max(0.0, min(CONSISTENCY_MAX_SCORE, score))


def _score_length(analyses: list[CommitAnalysis]) -> float:
    sample_size = len(analyses)
    if sample_size == 0:
        return 0.0

    per_commit_max = LENGTH_MAX_SCORE / sample_size
    total = sum(
        analysis.length_score_normalized * per_commit_max
        for analysis in analyses
    )
    return min(LENGTH_MAX_SCORE, total)


def _score_good_technical_terms(analyses: list[CommitAnalysis]) -> float:
    sample_size = len(analyses)
    if sample_size == 0:
        return 0.0

    qualifying_commits = 0
    for analysis in analyses:
        if analysis.good_terms_found:
            analysis.counted_for_good_terms = True
            qualifying_commits += 1

    score = qualifying_commits * (GOOD_PRACTICE_MAX_SCORE / sample_size)

    return min(GOOD_PRACTICE_MAX_SCORE, score)


def _score_bad_practices(analyses: list[CommitAnalysis]) -> float:
    occurrences = sum(
        len(analysis.bad_terms_found)
        for analysis in analyses
    )

    score = BAD_PRACTICE_MAX_SCORE - (occurrences * PER_BAD_PRACTICE_OCCURRENCE_PENALTY)

    return max(0.0, min(BAD_PRACTICE_MAX_SCORE, score))