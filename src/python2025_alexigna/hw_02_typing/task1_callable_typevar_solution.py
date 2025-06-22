from collections.abc import Callable, Sequence
from typing import TypeVar

SeqItemT = TypeVar("SeqItemT")
FuncResultT = TypeVar("FuncResultT")


def process(func: Callable[[SeqItemT], FuncResultT], seq: Sequence[SeqItemT]) -> list[FuncResultT]:
    return [func(item) for item in seq]


if __name__ == "__main__":
    for indx, (input_items, func, expected_result) in enumerate(
        (
            (
                (1, 2, 3, 4),
                lambda num: num**2,
                [1, 4, 9, 16],
            ),
            (
                ["a", "bb", "ccc"],
                len,
                [1, 2, 3],
            ),
            (
                ["a", "bb", "ccc"],
                str.upper,
                ["A", "BB", "CCC"],
            ),
        ),
        start=1,
    ):
        received_result = process(func, input_items)
        print(f"кейс {indx} - результат: {received_result}")
        print(f"кейс {indx} - ожидание : {expected_result}")
        assert received_result == expected_result
