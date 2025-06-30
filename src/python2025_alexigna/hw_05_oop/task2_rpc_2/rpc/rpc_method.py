from typing import Any

from rq import Queue
from rq.job import Job

from python2025_alexigna.hw_05_oop.task2_rpc_2.rpc.rpc_result import RPCResult


class RPCMethod:
    TASK_PREFIX = "tasks.task_"

    def __init__(self, queue: Queue, app_name: str, method_name: str) -> None:
        self._queue = queue
        self._app = app_name
        self._method = method_name

    def _enqueue(self, *args: Any, **kwargs: Any) -> RPCResult:
        job: Job = self._queue.enqueue(
            f=f"{self.TASK_PREFIX}{self._app}.{self._method}.{self._method}",
            args=args,
            kwargs=kwargs,
        )
        rpc_result = RPCResult(job)
        return rpc_result

    def __call__(self, *args: Any, **kwargs: Any) -> RPCResult:
        rpc_result = self._enqueue(*args, **kwargs)
        rpc_result.wait_for_result()
        return rpc_result

    def no_wait(self, *args: Any, **kwargs: Any) -> RPCResult:
        rpc_result = self._enqueue(*args, **kwargs)
        return rpc_result
