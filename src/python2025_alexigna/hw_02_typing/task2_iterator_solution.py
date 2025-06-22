from collections.abc import Iterator


def unrange_huawei_vlans(allow_pass_vlan_line: str) -> Iterator[int]:
    vlans = allow_pass_vlan_line.split("allow-pass vlan")[1].split()
    pointer = 0
    while pointer < len(vlans):
        start = vlans[pointer]
        end = vlans[pointer]
        pointer += 1
        if pointer < len(vlans) and vlans[pointer] == "to":
            end = vlans[pointer + 1]
            pointer += 2
        yield from range(int(start), int(end) + 1)


if __name__ == "__main__":
    for config_line, expected_vlan_list in (
        (
            "port trunk allow-pass vlan 10 to 15",
            [10, 11, 12, 13, 14, 15],
        ),
        (
            "port trunk allow-pass vlan 34 to 35 37 to 40 45 to 50",
            [34, 35, 37, 38, 39, 40, 45, 46, 47, 48, 49, 50],
        ),
        (
            "port trunk allow-pass vlan 100",
            [100],
        ),
        (
            "port trunk allow-pass vlan 100 110",
            [100, 110],
        ),
    ):
        received_vlan_list = list(unrange_huawei_vlans(config_line))
        print(f"{received_vlan_list=}")
        print(f"{expected_vlan_list=}")
        assert expected_vlan_list == received_vlan_list
