from functools import wraps
from typing import get_type_hints


def check_args_types(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        hints = get_type_hints(func)
        all_args = {**dict(zip(func.__code__.co_varnames, args)), **kwargs}
        for arg_name, arg_value in all_args.items():
            expected_type = hints.get(arg_name)
            if expected_type and not isinstance(arg_value, expected_type):
                raise TypeError(
                    f"Expected '{arg_name}' param to be "
                    f"{expected_type.__name__},"
                    f" got {type(arg_value).__name__} instead."
                )
        return func(*args, **kwargs)

    return wrapper
