from collections import defaultdict


def average_coalesce_strategy(data: list[dict[str, int]]) -> dict[str, int]:
    coalesced_data = defaultdict(int)
    data_length = len(data)

    for key in data[0].keys():
        coalesced_data[key] = int(sum([d[key] for d in data]) / data_length)

    return coalesced_data


def min_coalesce_strategy(data: list[dict[str, int]]) -> dict[str, int]:
    coalesced_data = defaultdict(int)

    for key in data[0].keys():
        coalesced_data[key] = min([d[key] for d in data])

    return coalesced_data


def max_coalesce_strategy(data: list[dict[str, int]]) -> dict[str, int]:
    coalesced_data = defaultdict(int)

    for key in data[0].keys():
        coalesced_data[key] = max([d[key] for d in data])

    return coalesced_data


STRATEGIES_MAPPING = {
    "avg": average_coalesce_strategy,
    "min": min_coalesce_strategy,
    "max": max_coalesce_strategy,
}

AVAILABLE_STRATEGIES = [key for key in STRATEGIES_MAPPING]


def coalesce_data(data: list[dict[str, int]], strategy: str) -> dict[str, int]:
    """
    Coalesce `data` based on the `strategy` defined.

    :param data: a list of dictionaries with the data to be coalesced.
    :param strategy: a string representing the strategy to be used to coalesce the data.
    :return: a dictionary with the coalesced data.
    """

    coalesce_strategy_function = STRATEGIES_MAPPING.get(strategy, average_coalesce_strategy)

    return coalesce_strategy_function(data)
