# регистрация протоколов

# сделать docker-compose
# разделить на файлы
# сделать raise_for_status
# добавить exceptions
# написать gather. as_completed на дз
# свести в ноль black/ruff/mypy
# написать pyi файл, добавить py.typed
# добавить описание функций
# перевести RPCResult на generic
# домашка:
#  - написать функцию-генератор as_completed
#  - добавить ограничение по времени в бесконечные циклы (wait_for_result, gather, ...)

import time
from types import TracebackType
from typing import Any, Literal, Self

from redis import Redis
from rq import Queue
from rq.job import Job, JobStatus


class RPCResult:
    def __init__(self, job: Job):
        self._job = job
        self._is_failed = False
        self._is_finished = False

    @property
    def result(self) -> Any:
        return self._job.result

    @property
    def is_failed(self) -> bool:
        return self._is_failed

    @property
    def is_finished(self) -> bool:
        return self._is_finished

    def update_status(self) -> None:
        status: JobStatus = self._job.get_status()
        # ошибка внутри функции (ZeroDivisionError: division by zero):
        #  - job.get_status() = JobStatus.FAILED
        #  - job.is_finished = False
        #  - job.job.is_failed = True
        #  - job.exc_info = traceback в текстовом виде
        match status:
            case JobStatus.QUEUED | JobStatus.STARTED:
                self._is_finished = False
                self._is_failed = False
            case JobStatus.FINISHED:
                self._is_finished = True
                self._is_failed = False
            case JobStatus.FAILED:
                self._is_finished = True
                self._is_failed = True
            case _:
                raise ValueError(f"неизвестный статус {self._job.id}: {status}")

    def wait_for_result(self) -> None:
        while not self._is_finished:
            time.sleep(0.5)
            self.update_status()


class RPCMethod:
    def __init__(self, queue: Queue, func_name: str) -> None:
        self._queue = queue
        self._func_name = func_name

    def __call__(self, *args, **kwargs) -> RPCResult:
        job: Job = self._queue.enqueue(
            f=f"tasks.{self._func_name}.{self._func_name}",
            args=args,
            kwargs=kwargs,
        )
        return RPCResult(job)


class RPC:
    def __init__(
        self,
        redis_host: str = "localhost",
        redis_port: int = 6379,
        redis_db: int = 0,
        redis_password: str | None = None,
    ) -> None:
        self._redis = Redis(redis_host, redis_port, redis_db, redis_password)

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> Literal[False]:
        self._redis.close()
        return False

    def __getattr__(self, name: str):
        queue = Queue(connection=self._redis)
        return RPCMethod(queue, name)
