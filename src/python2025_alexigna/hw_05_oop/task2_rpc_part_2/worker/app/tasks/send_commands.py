from typing import Any

from scrapli import Scrapli
from scrapli.response import MultiResponse

from python2025_alexigna.hw_05_oop.task2_rpc_part_2.rpc.utils import Platform

_scrapli_template = {
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_strict_key": False,
    "transport_options": {
        "open_cmd": [
            "-o",
            "KexAlgorithms=+diffie-hellman-group-exchange-sha1",
            "-o",
            "HostkeyAlgorithms=+ssh-rsa",
        ],
    },
}


def send_commands(
    platform: Platform,
    host: str,
    commands: list[str],
    *args: Any,
    **kwargs: Any,
) -> MultiResponse:
    scrapli = _scrapli_template | {"host": host, "platform": platform.value}
    with Scrapli(**scrapli) as cli:  # type: ignore [arg-type]
        response = cli.send_commands(commands, *args, **kwargs)
    return response
