import io  # noqa: F401
import os

from scrapli import Scrapli


def my_hello() -> None:
    print("hello")


def concat(a: str, b: str) -> str:
    """Конкатенация двух строк.

    Args:
        a (str): первая строка
        b (str): вторая строка


    Returns:
        str: результат конкатенации
    """
    f = "test"
    return a + b


if __name__ == "__main__":
    print(concat("11", "222"))
    print(f"hello")
    print(concat("11", "222"))
    print(f"hello")
