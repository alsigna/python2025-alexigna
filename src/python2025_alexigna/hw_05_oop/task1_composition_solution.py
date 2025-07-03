import weakref
from typing import Self
from weakref import WeakSet


class Device:
    def __init__(self, ip: str, asn: str) -> None:
        self.ip = ip
        self.asn = asn
        self.bgp = BGP(self)

    def add_peer(self, peer: Self) -> None:
        self.bgp.add_peering(peer)

    def __str__(self) -> str:
        return f"Device({self.ip}, {self.asn})"

    def __repr__(self) -> str:
        return str(self)

    def __del__(self) -> None:
        print(f"<< удаление объекта {self} >>")


class BGP:
    def __init__(self, device: Device) -> None:
        self._ip = device.ip
        self._device = weakref.ref(device)
        self._peers: WeakSet[Device] = WeakSet()

    @property
    def peers(self) -> set[Device]:
        return set(self._peers)

    @property
    def device(self) -> Device:
        device = self._device()
        if device is None:
            raise RuntimeError("BGP: родительский Device уничтожен")
        return device

    def add_peering(self, peer: Device) -> None:
        if peer is self.device:
            return
        self._peers.add(peer)
        peer.bgp._peers.add(self.device)  # noqa: SLF001

    def __str__(self) -> str:
        return f"BGP объект для Device({self._ip})"

    def __del__(self) -> None:
        print(f"<< удаление объекта {self} >>")


def demo() -> None:
    pe1 = Device("192.168.0.1", "64512")
    pe2 = Device("192.168.0.2", "64512")
    pe3 = Device("192.168.0.3", "64512")
    rr1 = Device("192.168.0.255", "64512")
    pe1.add_peer(rr1)
    pe1.add_peer(pe3)
    pe2.add_peer(rr1)
    pe3.add_peer(rr1)
    print(pe1.bgp.peers)
    print(pe2.bgp.peers)
    print(pe3.bgp.peers)
    print(rr1.bgp.peers)


if __name__ == "__main__":
    demo()
    print("= работа кода закончена =")
