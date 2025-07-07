import time
from typing import Generic, TypeVar

from rq.job import Job, JobStatus

from .exceptions import RPCFailedJobError

T = TypeVar("T")


class RPCResult(Generic[T]):
    def __init__(self, job: Job):
        self._job: Job = job
        self._job_id: str = job.id
        self._is_failed = False
        self._is_finished = False
        self._exc_info: str | None = None
        self._result: T | None = None

        description = self._job.description
        if description is None:
            self._description = "unknown task description"
        else:
            self._description = description.split(".", 2)[2]

    def __repr__(self) -> str:
        return f"[{self._job.id}] {self._description}"

    @property
    def result(self) -> T | None:
        return self._result

    @property
    def job_id(self) -> str:
        return self._job_id

    @property
    def is_failed(self) -> bool:
        self._update_status()
        return self._is_failed

    @property
    def is_finished(self) -> bool:
        self._update_status()
        return self._is_finished

    def _update_status(self) -> None:
        if self._is_finished:
            return
        status: JobStatus | None = self._job.get_status()
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
                self._result = self._job.result
            case JobStatus.FAILED:
                self._is_finished = True
                self._is_failed = True
                self._exc_info = self._job.exc_info
            case _:
                raise ValueError(f"неизвестный статус {self._job_id}: {status}")

    def raise_for_status(self) -> None:
        # fmt:off
        if (
            not self._is_finished  # задача еще не завершена
            or not self._is_failed  # или завершена, но без ошибок
        ):
            return
        # fmt:on
        raise RPCFailedJobError(self._exc_info) from None

    def wait_for_result(self) -> None:
        while not self._is_finished:
            time.sleep(0.5)
            self._update_status()
