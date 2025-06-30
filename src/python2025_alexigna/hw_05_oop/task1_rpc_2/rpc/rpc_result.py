import time
from typing import Any, cast

from rq.job import Job, JobStatus

from python2025_alexigna.hw_05_oop.task1_rpc_2.rpc.exceptions import RPCFailedJobError, RPCJobStatusError


class RPCResult:
    def __init__(self, job: Job) -> None:
        self._job = job
        self._is_failed = False
        self._is_finished = False
        self._exception: Exception | None = None

    def _update_status(self) -> None:
        if self._is_finished:
            return
        status: JobStatus | None = self._job.get_status()
        if status is None:
            raise RPCJobStatusError(f"невозможно определить статус job: {self._job.id}")
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
                try:
                    self._job.func()
                except Exception as exc:
                    self._exception = exc
            case _:
                raise ValueError(f"неизвестный статус '{self._job.id}': '{status}'")

    def wait_for_result(self) -> None:
        while not self._is_finished:
            self._update_status()
            time.sleep(1)

    def raise_for_status(self) -> None:
        if not self._is_finished or not self._is_failed or self._exception is None:
            return
        # при исключении в worker'е
        # job.result -> None
        # job.exc_info -> traceback в виде текста
        # job.func() -> бросает исключение, которое было вызвано в worker
        raise RPCFailedJobError(str(self._exception)) from self._exception

    @property
    def result(self) -> Any:
        if self._is_finished:
            return self._job.result
        else:
            return None

    @property
    def exception(self) -> Exception | None:
        self._update_status()
        return self._exception

    @property
    def is_failed(self) -> bool:
        self._update_status()
        return self._is_failed

    @property
    def is_finished(self) -> bool:
        self._update_status()
        return self._is_finished

    @property
    def job_id(self) -> str:
        return cast(str, self._job.id)
