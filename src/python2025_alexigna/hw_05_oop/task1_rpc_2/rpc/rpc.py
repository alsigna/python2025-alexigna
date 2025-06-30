import time
from types import TracebackType
from typing import Literal, Self, Sequence

from redis import Redis
from rq import Queue

from python2025_alexigna.hw_05_oop.task1_rpc_2.rpc.rpc_method import RPCMethod
from python2025_alexigna.hw_05_oop.task1_rpc_2.rpc.rpc_result import RPCResult


class RPC:
    def __init__(
        self,
        app_name: str,
        redis_host: str = "localhost",
        redis_port: int = 6379,
        redis_db: int = 0,
        redis_password: str | None = None,
        redis_queue_name: str = "be",
    ):
        self._app_name = app_name
        self._queue_name = redis_queue_name
        self._redis = Redis(redis_host, redis_port, redis_db, redis_password)

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> Literal[False]:
        self._redis_close()
        return False

    def __del__(self) -> None:
        self._redis_close()

    def _redis_close(self) -> None:
        if hasattr(self, "_redis") and self._redis:
            self._redis.close()
            self._redis = None

    def __getattr__(self, method: str) -> RPCMethod:
        queue = Queue(name=self._queue_name, connection=self._redis)
        return RPCMethod(
            queue=queue,
            app_name=self._app_name,
            method_name=method,
        )

    def _gather(self, tasks: Sequence[RPCResult]) -> bool:
        for task in tasks:
            if not task.is_finished:
                return False
        return True

    def gather(self, tasks: Sequence[RPCResult]) -> None:
        while True:
            if self._gather(tasks):
                return
            time.sleep(0.5)
