from typing import Any

from scrapli import Scrapli
from scrapli.response import Response

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


def send_command(
    platform: str,
    host: str,
    command: str,
    *args: Any,
    **kwargs: Any,
) -> Response:
    scrapli = _scrapli_template | {"host": host, "platform": platform}
    with Scrapli(**scrapli) as cli:  # type: ignore [arg-type]
        response = cli.send_command(command, *args, **kwargs)
    return response
