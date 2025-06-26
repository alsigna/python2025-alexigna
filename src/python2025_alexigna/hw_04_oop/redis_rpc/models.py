from enum import StrEnum, auto


class TaskStatus(StrEnum):
    QUEUED = auto()
    STARTED = auto()
    FINISHED = auto()
    FAILED = auto()
    UNKNOWN = auto()
