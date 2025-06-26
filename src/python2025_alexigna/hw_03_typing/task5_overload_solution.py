from typing import overload


@overload
def parse_value(value: str) -> int | float: ...


@overload
def parse_value(value: int | float) -> str: ...


def parse_value(value: int | float | str) -> int | float | str:
    if isinstance(value, str):
        return float(value) if "." in value else int(value)
    return str(value)


if __name__ == "__main__":
    assert parse_value("123") == 123
    assert parse_value("3.14") == 3.14
    assert parse_value(42) == "42"
    assert parse_value(3.14) == "3.14"
