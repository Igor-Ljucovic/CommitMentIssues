import random


def random_list_sample(
    samples: list[str],
    sample_size: int,
    seed: int | None,
) -> list[str]:
    if sample_size <= 0:
        raise ValueError("sample_size must be greater than 0.")

    if not samples:
        return []

    actual_size = min(sample_size, len(samples))
    rng = random.Random(seed)
    return rng.sample(samples, actual_size)