from random import randint
from time import perf_counter, sleep
from typing import Any


def send_command(
    hostname: str,
    platform: str,
    command: str,
    *args,
    **kwargs,
) -> dict[str, Any]:
    t0 = perf_counter()
    sleep(randint(50, 200) / 100)
    return {
        "host": hostname,
        "platform": platform,
        "command": command,
        "output": "some text from device",
        "elapsed_time": round(perf_counter() - t0, 3),
    }
