from time import perf_counter
from typing import Any

from scrapli import Scrapli
from scrapli.response import MultiResponse, Response

device = {
    "platform": "cisco_iosxe",
    "host": "192.168.122.101",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_strict_key": False,
    "transport": "paramiko",
}


def _send_and_read(ssh: Scrapli, command: str) -> MultiResponse:
    result = MultiResponse()
    cmd: str | None = command
    while cmd is not None:
        output: Response = ssh.send_and_read(
            channel_input=cmd,
            expected_outputs=[
                ssh.comms_prompt_pattern,
                r"\[confirm\]",
                r"\[yes/no\]",
            ],
            timeout_ops=30,
            read_duration=10,
        )
        result.append(output)
        if output.result.endswith("[confirm]"):
            cmd = "\n"
        elif output.result.endswith("[yes/no]:"):
            cmd = "yes"
        else:
            cmd = None
    return result


def send_command(device: dict[str, Any], command: str) -> None:
    with Scrapli(
        **device,
        channel_log="./debug.log",
    ) as ssh:
        outputs = _send_and_read(ssh, command)
    print(outputs.result)


def send_commands(device: dict[str, Any], commands: list[str]) -> None:
    with Scrapli(
        **device,
        channel_log="./debug.log",
    ) as ssh:
        result = MultiResponse()
        for command in commands:
            result.extend(_send_and_read(ssh, command))
    print(result.result)


if __name__ == "__main__":
    t0 = perf_counter()
    try:
        # send_command(device, "reload in 30")
        send_commands(
            device,
            [
                "clear logging",
                "show version",
                "reload in 30",
                "write",
                "reload cancel",
            ],
        )
    except Exception as exc:
        print(f"exception class: {exc.__class__.__name__}")
        print(f"exception message: {str(exc)}")
    finally:
        print(f"\nelapsed time: {perf_counter() - t0:.4f} sec")
