import time
from random import randint
from typing import Any

from scrapli.response import Response


def send_command(host: str, command: str, *arg: Any, **kwargs: Any) -> Response:
    print(f"собираем вывод '{command}' с '{host}' ... (текст внутри функции)")
    response = Response(
        host=host,
        channel_input=command,
    )
    time.sleep(randint(50, 200) / 100)
    # return f"вывод '{command}' с '{host}' (возвращаемое значение)"
    return response
