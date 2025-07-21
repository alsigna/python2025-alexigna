from typing import Any, Generic, TypeVar

from redis import Redis

T = TypeVar("T")


class Singleton(type, Generic[T]):
    _INSTANCES: dict["Singleton[T]", T] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> T:
        if cls not in cls._INSTANCES:
            cls._INSTANCES[cls] = super().__call__(*args, **kwargs)
        return cls._INSTANCES[cls]


class RPCRedis(metaclass=Singleton):
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: str | None = None,
    ) -> None:
        self.redis = Redis(host, port, db, password)
