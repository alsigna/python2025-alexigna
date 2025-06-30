class RPCError(Exception):
    """Общая ошибка приложения."""


class RPCFailedJobError(RPCError):
    """Job в статусе FAILED."""


class RPCJobStatusError(RPCError):
    """Статус Job вернулся None."""
