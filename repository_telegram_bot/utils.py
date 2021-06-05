"""This file contains utils methods."""
from typing import Any, Dict, Optional


def deep_get(obj: Optional[Dict[str, Any]], path: str) -> Any:
    """
    Return value from dict by string path or None.

    :param obj:
    :param path:
    :return:
    """
    accumulator: Any = obj
    for prop in path.split('.'):
        if isinstance(accumulator, dict):
            accumulator = accumulator.get(prop, None)
        else:
            accumulator = None
    return accumulator

    # return next(
    #     reduce(
    #         lambda dict_, attr: dict_.get(attr) if isinstance(dict_, dict) else None,
    #         path.split('.'),
    #         obj,
    #     )
    # )
