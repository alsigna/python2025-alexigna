from enum import StrEnum, auto
from typing import assert_never


class Vendor(StrEnum):
    CISCO = auto()
    HUAWEI = auto()
    ARISTA = auto()


def svi_name(vendor: Vendor, svi_id: int) -> str:
    if vendor == Vendor.CISCO:
        return f"Vlan{svi_id}"
    elif vendor == Vendor.HUAWEI:
        return f"Vlanif{svi_id}"
    elif vendor == Vendor.ARISTA:
        return f"Vlan{svi_id}"
    else:
        assert_never(vendor)
        raise NotImplementedError(vendor)


if __name__ == "__main__":
    assert svi_name(Vendor.CISCO, 10) == "Vlan10"
    assert svi_name(Vendor.HUAWEI, 10) == "Vlanif10"
    assert svi_name(Vendor.ARISTA, 10) == "Vlan10"
