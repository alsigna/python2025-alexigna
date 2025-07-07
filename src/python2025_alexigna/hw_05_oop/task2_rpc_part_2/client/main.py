from abc import ABC, abstractmethod
from typing import ClassVar

from python2025_alexigna.hw_05_oop.task2_rpc_part_2.rpc import RPC
from python2025_alexigna.hw_05_oop.task2_rpc_part_2.rpc.utils import Platform


class Device(ABC):
    platform: ClassVar[Platform]

    def __init__(self, host: str):
        self.host = host

    @property
    @abstractmethod
    def commands(self) -> list[str]: ...

    def __init_subclass__(cls):
        super().__init_subclass__()
        if not hasattr(cls, "platform") or not isinstance(cls.platform, Platform):
            raise TypeError(f"Класс {cls.__name__} должен определить `platform: ClassVar[Platform]`")


class CiscoIOSXE(Device):
    platform = Platform.CISCO_IOSXE
    commands = ["show version", "show inventory"]


class HuaweiVRP(Device):
    platform = Platform.HUAWEI_VRP
    commands = ["display version", "display device"]


class DeviceFactory:
    platform_map = {
        Platform.CISCO_IOSXE: CiscoIOSXE,
        Platform.HUAWEI_VRP: HuaweiVRP,
    }

    @classmethod
    def create(cls, platform: Platform, host: str) -> Device:
        if platform not in cls.platform_map:
            raise ValueError(f"неизвестная платформа '{platform}'")
        return cls.platform_map[platform](host)


devices = [
    DeviceFactory.create(Platform.CISCO_IOSXE, "192.168.122.101"),
    DeviceFactory.create(Platform.CISCO_IOSXE, "192.168.122.102"),
    DeviceFactory.create(Platform.HUAWEI_VRP, "192.168.122.103"),
]

with RPC() as rpc:
    #     # result: RPCResult = rpc.hello(user="admin", count=3)
    #     # print(f"{result.job_id=}")
    #     # result.wait_for_result()
    #     # result.raise_for_status()
    #     # print(f"{result.result=}")
    #     # print(f"{result.is_failed=}")
    #     # print(f"{result.is_finished=}")

    #     str_tasks = [rpc.hello(user=user, count=1) for user in ["admin", "alice", "bob", "john"]]
    #     rpc.gather(*str_tasks)
    #     for str_task in str_tasks:
    #         print(str_task.result)

    #     scrapli_tasks = [
    #         rpc.send_command(host, "cisco_iosxe", "show version") for host in ("192.168.122.101", "192.168.122.102")
    #     ]
    #     rpc.gather(*scrapli_tasks)
    #     for scrapli_task in scrapli_tasks:
    #         scrapli_task.raise_for_status()
    #         if scrapli_task.result is None:
    #             continue
    #         print("-" * 20)
    #         print(f"{scrapli_task.job_id=}")
    #         print(f"{scrapli_task.is_finished=}")
    #         print(f"{scrapli_task.is_failed=}")
    #         print(f"{scrapli_task.result.host=}")
    #         print(f"{scrapli_task.result.channel_input=}")
    #         print(f"{scrapli_task.result.result}")
    #         print(f"{scrapli_task.result.channel_input=}")
    #         print(f"{scrapli_task.result.result}")
    #         print(f"{scrapli_task.result.channel_input=}")
    #         print(f"{scrapli_task.result.result}")
    #         print(f"{scrapli_task.result.result}")

    tasks = [rpc.send_commands(device.platform, device.host, device.commands) for device in devices]
    rpc.gather(*tasks)
    for task in tasks:
        task.raise_for_status()
        if task.result is None:
            continue
        print(task.result.result)
        print(task.result.result)
