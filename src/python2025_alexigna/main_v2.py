from typing import Any, Protocol

from scrapli import Scrapli

from python2025_alexigna.config import config
from python2025_alexigna.utils import Parameter

if config.developer_mode:
    import logging

    log = logging.getLogger("scrapli")
    log.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    log.addHandler(sh)


class Device(Protocol):
    class Config:
        cli_username: Parameter[str] = Parameter(env="MY_APP_CLI_USERNAME", type_=str)
        cli_password: Parameter[str] = Parameter(env="MY_APP_CLI_PASSWORD", type_=str)
        scrapli_cli_transport: Parameter[str] = Parameter(env="MY_APP_CLI_SCRAPLI_TRANSPORT", default="system")
        scrapli_cli_port: Parameter[int] = Parameter(env="MY_APP_CLI_SCRAPLI_PORT", default=22)
        scrapli_timeout_socket: Parameter[int] = Parameter(env="MY_APP_SCRAPLI_TIMEOUT_SOCKET", default=15)
        scrapli_timeout_transport: Parameter[int] = Parameter(env="MY_APP_SCRAPLI_TIMEOUT_TRANSPORT", default=30)
        scrapli_timeout_ops: Parameter[int] = Parameter(env="MY_APP_SCRAPLI_TIMEOUT_OPS", default=30)

    platform: str
    show_version_command: str

    def __init__(
        self,
        ip: str,
        port: int | None = None,
        transport: str | None = None,
    ):
        self.ip = ip
        self.spec = self.Config()

    @property
    def scrapli(self) -> dict[str, Any]:
        return {
            "platform": self.platform,
            "host": self.ip,
            "port": self.spec.scrapli_cli_port,
            "transport": self.spec.scrapli_cli_transport,
            "auth_username": self.spec.cli_username,
            "auth_password": self.spec.cli_password,
            "auth_secondary": self.spec.cli_password,
            "auth_strict_key": False,
            "ssh_config_file": True,
            "timeout_socket": self.spec.scrapli_timeout_socket,
            "timeout_transport": self.spec.scrapli_timeout_transport,
            "timeout_ops": self.spec.scrapli_timeout_ops,
        }

    def get_version_output(self) -> str:
        with Scrapli(
            **self.scrapli,
            channel_log=config.dump_to_file,
            channel_log_mode="append" if config.dump_to_file else None,
        ) as cli:
            output = cli.send_command(
                self.show_version_command,
            )
        if config.dump_to_file:
            with open(f"./{self.ip}-{self.show_version_command}.txt", "w") as f:
                f.write(output.result)
        return output.result


class CiscoIOSXE(Device):
    platform = "cisco_iosxe"
    show_version_command = "show version"


class HuaweiVRP(Device):
    platform = "huawei_vrp"
    show_version_command = "display version"


class DeviceFactory:
    _PLATFORM_MAP: dict[str, type[Device]] = {
        "cisco_iosxe": CiscoIOSXE,
        "huawei_vrp": HuaweiVRP,
    }

    @classmethod
    def create(cls, ip: str, platform: str) -> Device:
        if platform not in cls._PLATFORM_MAP:
            raise ValueError(f"Unknown platform '{platform}'")
        return cls._PLATFORM_MAP[platform](ip)


if __name__ == "__main__":
    for device in (
        DeviceFactory.create("192.168.122.101", "cisco_iosxe"),
        DeviceFactory.create("192.168.122.102", "cisco_iosxe"),
        DeviceFactory.create("192.168.122.103", "huawei_vrp"),
    ):
        if device.ip == "192.168.122.102":
            device.spec.scrapli_cli_transport = "telnet"
            device.spec.scrapli_cli_port = 23
        print(device.get_version_output())
