from collections import defaultdict
from typing import Callable


def average_coalescing_strategy(data: list[dict[str, int]]) -> dict[str, int]:
    coalesced_data = defaultdict(int)
    data_length = len(data)

    for key in data[0].keys():
        coalesced_data[key] = int(sum([d[key] for d in data]) / data_length)

    return coalesced_data


def min_coalescing_strategy(data: list[dict[str, int]]) -> dict[str, int]:
    coalesced_data = defaultdict(int)

    for key in data[0].keys():
        coalesced_data[key] = min([d[key] for d in data])

    return coalesced_data


def max_coalescing_strategy(data: list[dict[str, int]]) -> dict[str, int]:
    coalesced_data = defaultdict(int)

    for key in data[0].keys():
        coalesced_data[key] = max([d[key] for d in data])

    return coalesced_data


def get_strategy(strategy: str) -> Callable[[list[dict[str, int]]], dict[str, int]]:
    strategies_mapping = {
        "avg": average_coalescing_strategy,
        "min": min_coalescing_strategy,
        "max": max_coalescing_strategy,
    }

    return strategies_mapping.get(strategy, average_coalescing_strategy)
