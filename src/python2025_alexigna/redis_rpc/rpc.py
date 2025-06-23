import time
from typing import Any, Callable, Literal, Protocol, TypeAlias, overload

from redis import Redis
from rq import Queue
from rq.exceptions import InvalidJobOperation
from rq.job import Job, NoSuchJobError
from scrapli import Scrapli
from scrapli.response import Response

from python2025_alexigna.redis_rpc.models import TaskStatus


class RpcReply:
    def __init__(
        self,
        redis: Redis,
        task_id: str,
        polling_interval: float | None = None,
        timeout: float | None = None,
    ) -> None:
        self.id: str = task_id
        self.redis = redis
        self._task: Job | None = None
        self._status: TaskStatus = TaskStatus.QUEUED
        self.polling_interval = polling_interval or 1.0
        self.timeout = timeout

    @property
    def task(self) -> Job:
        if self._task is None:
            try:
                self._task = Job.fetch(id=self.id, connection=self.redis)
            except NoSuchJobError as exc:
                self._status = TaskStatus.UNKNOWN
                raise exc
        return self._task

    @property
    def status(self) -> TaskStatus:
        # queued -> started -> finished/failed. unknown если job не найдена
        if self._status in [TaskStatus.FINISHED, TaskStatus.FAILED, TaskStatus.UNKNOWN]:
            return self._status

        try:
            status = self.task.get_status()
        except InvalidJobOperation:
            return TaskStatus.UNKNOWN

        if status is None:
            return TaskStatus.UNKNOWN
        self._status = TaskStatus(status)
        return self._status

    @property
    def result(self) -> dict[str, Any]:
        try:
            return self.task.result or {}
        except (InvalidJobOperation, NoSuchJobError):
            self._status = TaskStatus.UNKNOWN
            return {"error": "Task not available"}

    @property
    def meta(self) -> dict[str, Any]:
        try:
            return self.task.meta or {}
        except (InvalidJobOperation, NoSuchJobError):
            self._status = TaskStatus.UNKNOWN
            return {}

    def wait_for_result(self) -> dict[str, Any]:
        status = TaskStatus.QUEUED
        t0 = time.time()
        while status not in [TaskStatus.FAILED, TaskStatus.FINISHED, TaskStatus.UNKNOWN]:
            status = self.status
            if self.timeout and (time.time() - t0) > self.timeout:
                self._status = TaskStatus.UNKNOWN
                raise TimeoutError("Timeout ожидания результатов задачи")
            time.sleep(self.polling_interval)
        self._status = TaskStatus.FINISHED
        return self.task.result or {}


class ProxyMethod:
    TASK_PREFIX = "tasks.task_"

    def __init__(
        self,
        redis: Redis,
        app_name: str,
        task_name: str,
        queue: str,
    ) -> None:
        self.app_name = app_name
        self.task_name = task_name
        self.queue = queue
        self.task: Job | None = None
        self.redis = redis

    def _enqueue(self, *args: Any, **kwargs: Any) -> Job:
        queue = Queue(connection=self.redis, name=self.queue)
        meta = kwargs.pop("meta", {})
        task: Job = queue.enqueue(
            f=f"{self.TASK_PREFIX}{self.app_name}.{self.task_name}",
            meta=meta,
            args=args,
            kwargs=kwargs,
        )
        self.task = task
        print(f"{task=}")
        print(f"{args=}")
        print(f"{kwargs=}")
        return task

    def no_wait(self, *args: Any, **kwargs: Any) -> RpcReply:
        timeout = kwargs.pop("timeout", None)
        task = self._enqueue(*args, **kwargs)
        polling_interval = kwargs.pop("polling_interval", None)
        reply = RpcReply(
            redis=self.redis,
            task_id=task.id,
            polling_interval=polling_interval,
            timeout=timeout,
        )
        return reply

    def __call__(self, *args: Any, **kwargs: Any) -> RpcReply:
        reply = self.no_wait(*args, **kwargs)
        reply.wait_for_result()
        return reply


class ProxyRPC:
    def __init__(
        self,
        redis: Redis,
        app_name: str = "scrapli",
        queue: Literal["be", "pq"] = "be",
    ) -> None:
        self.app_name = app_name
        self.queue = queue
        self.redis = redis

    def __getattr__(self, task_name: str) -> Callable[..., Any]:
        return ProxyMethod(
            app_name=self.app_name,
            task_name=task_name,
            queue=self.queue,
            redis=self.redis,
        )


if __name__ == "__main__":
    with Redis() as redis:
        rpc = ProxyRPC(redis)
        result = rpc.send_command({"host": "1.2.3.4"}, "show version")
