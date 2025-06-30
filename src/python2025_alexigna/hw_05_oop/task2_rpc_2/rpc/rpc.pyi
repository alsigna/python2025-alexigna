from types import TracebackType
from typing import Literal, Self, Sequence

from python2025_alexigna.hw_05_oop.task2_rpc_2.rpc.rpc_method import RPCMethod
from python2025_alexigna.hw_05_oop.task2_rpc_2.rpc.rpc_result import (
    RPCResult,
    ScrapliSendCommandRPCResult,
    ScrapliSendCommandsRPCResult,
)

class RPC:
    def __init__(
        self,
        app_name: str,
        redis_host: str = "localhost",
        redis_port: int = 6379,
        redis_db: int = 0,
        redis_password: str | None = None,
        redis_queue_name: str = "be",
    ) -> None: ...
    def __enter__(self) -> Self: ...
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> Literal[False]: ...
    def __del__(self) -> None: ...
    def __getattr__(self, method: str) -> RPCMethod: ...
    def gather(self, tasks: Sequence[RPCResult]) -> None: ...
    def send_command(self, host: str, command: str) -> ScrapliSendCommandRPCResult: ...
    def send_commands(self, host: str, commands: Sequence[str]) -> ScrapliSendCommandsRPCResult: ...
