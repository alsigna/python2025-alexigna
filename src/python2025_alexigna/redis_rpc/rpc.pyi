from typing import Any, Callable, Literal, TypeAlias

from _typeshed import Incomplete
from redis import Redis
from rq.job import Job
from scrapli import Scrapli
from scrapli.response import Response

from python2025_alexigna.redis_rpc.models import TaskStatus as TaskStatus
from python2025_alexigna.redis_rpc.storage import RedisRPC as RedisRPC

class RpcReply:
    id: str
    redis: Incomplete
    polling_interval: Incomplete
    timeout: Incomplete
    def __init__(
        self, redis: Redis, task_id: str, polling_interval: float | None = None, timeout: float | None = None
    ) -> None: ...
    @property
    def task(self) -> Job: ...
    @property
    def status(self) -> TaskStatus: ...
    @property
    def result(self) -> dict[str, Any]: ...
    @property
    def meta(self) -> dict[str, Any]: ...
    def wait_for_result(self) -> dict[str, Any]: ...

class ProxyMethod:
    TASK_PREFIX: str
    app_name: Incomplete
    task_name: Incomplete
    queue: Incomplete
    task: Job | None
    redis: Incomplete
    def __init__(self, redis: Redis, app_name: str, task_name: str, queue: str) -> None: ...
    def no_wait(self, *args: Any, **kwargs: Any) -> RpcReply: ...
    def __call__(self, *args: Any, **kwargs: Any) -> RpcReply: ...

class ProxyRPC:
    app_name: Incomplete
    queue: Incomplete
    redis: Incomplete
    def __init__(
        self,
        redis: Redis,
        app_name: str = "scrapli",
        queue: Literal["be", "pq"] = "be",
    ) -> None: ...
    def send_command(
        self,
        hostname: str,
        platform: str,
        command: str,
        /,
        polling_interval: float | None = None,
        timeout: float | None = None,
    ) -> Response: ...
