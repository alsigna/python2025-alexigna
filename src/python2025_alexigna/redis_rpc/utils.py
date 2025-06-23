from typing import Any, Generic, TypeVar

T = TypeVar("T")


class Singleton(type, Generic[T]):
    _INSTANCES: dict["Singleton[T]", T] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> T:
        if cls not in cls._INSTANCES:
            cls._INSTANCES[cls] = super().__call__(*args, **kwargs)
        return cls._INSTANCES[cls]
