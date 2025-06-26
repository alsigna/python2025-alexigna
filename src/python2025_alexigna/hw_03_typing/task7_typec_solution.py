import logging
import os
from enum import StrEnum, auto
from types import TracebackType
from typing import Any, Literal, Self, TypeAlias, cast

from scrapli import Scrapli
from scrapli.exceptions import ScrapliException
from scrapli.response import Response

ScrapliDict: TypeAlias = dict[Any, Any]


USERNAME = os.getenv("SCRAPLI_USERNAME")
PASSWORD = os.getenv("SCRAPLI_PASSWORD")

if USERNAME is None or PASSWORD is None:
    USERNAME = "admin"
    PASSWORD = "P@ssw0rd"  # noqa: S105
    # raise ValueError("Отсутствуют USERNAME/PASSWORD")


class Transport(StrEnum):
    SYSTEM = auto()
    TELNET = auto()
    PARAMIKO = auto()


class Platform(StrEnum):
    HUAWEI_VRP = auto()
    CISCO_IOSXE = auto()
    ARISTA_EOS = auto()


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
fmt = logging.Formatter(
    fmt="%(asctime)s - [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
sh.setFormatter(fmt)
log.addHandler(sh)


class DeviceABC:
    SCRAPLI_TIMEOUT_OPS = 120
    SCRAPLI_TIMEOUT_SOCKET = 30
    SCRAPLI_TIMEOUT_TRANSPORT = 30

    def __init__(
        self,
        hostname: str,
        username: str,
        password: str,
        transport: Transport = Transport.SYSTEM,
    ) -> None:
        self.hostname = hostname
        self.username = username
        self.password = password
        self.transport = transport
        self._cli: Scrapli = Scrapli(**self._scrapli)

    def __enter__(self) -> Self:
        """Вход в контекстный менеджер."""
        self.open()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> Literal[False]:
        """Выход из контекстного менеджера."""
        self.close()
        return False

    def open(self) -> None:
        if not self._cli.isalive():
            try:
                self._cli.open()
            except ScrapliException as exc:
                log.exception(
                    "{}: ошибка открытия сессии, {}: {}".format(
                        self.hostname,
                        exc.__class__.__name__,
                        str(exc),
                    ),
                )
                raise exc
            except Exception as exc:
                log.exception(
                    "{}: неизвестная ошибка ошибка открытия сессии, {}: {}".format(
                        self.hostname,
                        exc.__class__.__name__,
                        str(exc),
                    ),
                )
                raise exc
            else:
                log.debug(f"{self.hostname}: сессия с устройством открыта")

    def close(self) -> None:
        try:
            self._cli.close()
        except Exception as exc:
            log.warning(
                "{}: ошибка закрытия сессии, {}: {}".format(
                    self.hostname,
                    exc.__class__.__name__,
                    str(exc),
                ),
            )
        else:
            log.debug(f"{self.hostname}: сессия с устройством закрыта")

    def send_command(self, command: str, **kwargs: Any) -> Response:
        output = self._cli.send_command(command, **kwargs)
        if output.failed:
            log.fatal(f"{self.hostname}: ошибка сбора команды '{command}':\n{output.channel_input}\n{output.result}")
        else:
            log.info(f"{self.hostname}: команда '{command}' успешно собрана")
        return output

    def get_show_version(self) -> str:
        output = self.send_command(self.show_version_command)
        return output.result

    @property
    def show_version_command(self) -> str:
        raise NotImplementedError("Требуется определить атрибут")

    @property
    def platform(self) -> Platform:
        raise NotImplementedError("Требуется определить атрибут")

    @property
    def _scrapli(self) -> ScrapliDict:
        return {
            "auth_username": self.username,
            "auth_password": self.password,
            "auth_secondary": self.password,
            "platform": self.platform,
            "transport": self.transport,
            "host": self.hostname,
            "auth_strict_key": False,
            "port": 23 if self.transport == Transport.TELNET else 22,
            "transport_options": {
                "open_cmd": [
                    "-o",
                    "KexAlgorithms=+diffie-hellman-group1-sha1,diffie-hellman-group14-sha1,diffie-hellman-group-exchange-sha1",
                    "-o",
                    "HostKeyAlgorithms=+ssh-rsa",
                ],
            },
            "timeout_ops": self.SCRAPLI_TIMEOUT_OPS,
            "timeout_socket": self.SCRAPLI_TIMEOUT_SOCKET,
            "timeout_transport": self.SCRAPLI_TIMEOUT_TRANSPORT,
        }


class HuaweiVRP(DeviceABC):
    show_version_command = "display version"
    platform = Platform.HUAWEI_VRP


class CiscoIOSXE(DeviceABC):
    show_version_command = "show version"
    platform = Platform.CISCO_IOSXE


class Device(DeviceABC):
    PLATFORM_MAP: dict[Platform, type[DeviceABC]] = {
        Platform.HUAWEI_VRP: HuaweiVRP,
        Platform.CISCO_IOSXE: CiscoIOSXE,
    }

    def __new__(
        cls,
        hostname: str,
        username: str,
        password: str,
        platform: Platform,
        transport: Transport = Transport.SYSTEM,
    ) -> "Device":
        if platform not in cls.PLATFORM_MAP:
            raise ValueError(f"неизвестная платформа '{platform}'")
        _device_class: type[DeviceABC] = cls.PLATFORM_MAP[platform]
        device = _device_class(
            hostname=hostname,
            username=username,
            password=password,
            transport=transport,
        )
        device = cast(Device, device)
        return device


devices: list[DeviceABC] = [
    Device(
        hostname="192.168.122.101",
        username=USERNAME,
        password=PASSWORD,
        transport=Transport.SYSTEM,
        platform=Platform.CISCO_IOSXE,
    ),
    Device(
        hostname="192.168.122.107",
        username=USERNAME,
        password=PASSWORD,
        transport=Transport.SYSTEM,
        platform=Platform.HUAWEI_VRP,
    ),
]
for device in devices:
    with device as ssh:
        print(ssh.get_show_version())
