from redis import Redis

from python2025_alexigna.redis_rpc.utils import Singleton


class RedisRPC(metaclass=Singleton):
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: str | None = None,
    ) -> None:
        self.redis = Redis(
            host=host,
            port=port,
            db=db,
            password=password,
        )

    def __enter__(self) -> Redis:
        return self.redis

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            self.redis.close()
        except Exception as exc:
            pass
        return False


if __name__ == "__main__":
    # r = RedisRPC()
    # r.connection.set("foo", "bar")  # Записываем ключ 'foo' со значением 'bar'
    # value = r.connection.get("foo")  # Получаем значение по ключу 'foo'
    # print(value)  # Выведет: b'bar' (префикс b означает bytes)

    with RedisRPC() as redis:
        value = redis.get("foo")
        print(value)
