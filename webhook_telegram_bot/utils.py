"""This file contains utils methods."""
from functools import reduce
from typing import Any, Dict, Optional


def deep_get(obj: Optional[Dict[str, Any]], path: str) -> Any:
    """
    Return value from dict by string path or None.

    :param obj:
    :param path:
    :return:
    """
    # accumulator: Any = obj
    # for prop in path.split('.'):
    #     if isinstance(accumulator, dict):
    #         accumulator = accumulator.get(prop, None)
    #     else:
    #         accumulator = None
    # return accumulator

    return reduce(
        lambda acc, curr: acc.get(curr, None) if isinstance(acc, Dict) else None,
        path.split('.'),
        obj,
    )
