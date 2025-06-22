from collections.abc import Callable, Mapping
from functools import lru_cache
from types import MappingProxyType
from typing import TypeAlias
from urllib.parse import urlencode

# from typing import TypeAlias
QueryParam: TypeAlias = tuple[str, str | int]
# type QueryParam = tuple[str, str | int]

NETBOX_URL = "https://demo.netbox.dev"


EXAMPLE_INPUT = MappingProxyType(
    {
        "manufacturer": ["cisco"],
        "role": ["router", "core-switch", "access-switch"],
        "status": ["active", "offline"],
        "site": ["dm-akronsk", "dm-albany", "dm-camden"],
    },
)

EXAMPLE_RESULT = (
    ("manufacturer_id", 3),
    ("role_id", 1),
    ("role_id", 2),
    ("role_id", 4),
    ("status", "active"),
    ("status", "offline"),
    ("site_id", 2),
    ("site_id", 3),
    ("site_id", 6),
    ("brief", "true"),
    ("limit", 500),
)


@lru_cache
def _get_site_id(site_slug: str) -> int:
    """Заглушка для получения id сайта по slug."""
    site_id = {
        "dm-akronsk": 2,
        "dm-albany": 3,
        "dm-binghamton": 4,
        "dm-buffalo": 5,
        "dm-camden": 6,
    }.get(site_slug)
    if site_id is None:
        msg = f"неизвестный сайт '{site_slug}'"
        raise ValueError(msg)
    return site_id


@lru_cache
def _get_device_role_id(device_role_slug: str) -> int:
    """Заглушка для получения id роли устройства по её slug."""
    device_role_id = {
        "router": 1,
        "core-switch": 2,
        "distribution-switch": 3,
        "access-switch": 4,
    }.get(device_role_slug)
    if device_role_id is None:
        msg = f"неизвестная роль устройства '{device_role_slug}'"
        raise ValueError(msg)
    return device_role_id


@lru_cache
def _get_manufacturer_id(manufacturer_slug: str) -> int:
    manufacturer_id = {
        "arista": 1,
        "cisco": 3,
        "juniper": 7,
    }.get(manufacturer_slug)
    if manufacturer_id is None:
        msg = f"неизвестный производитель '{manufacturer_slug}'"
        raise ValueError(msg)
    return manufacturer_id


def craft_nb_query(
    request_params: Mapping[str, list[str]],
) -> list[QueryParam]:
    """Преобразование набора параметров в request params.

    Args:
        request_params (Mapping[str, list[str]]): параметры запроса.
        ```python
        {
            "manufacturer": ["cisco"],
            "role": ["router"],
            "status": ["active", "offline"],
            "site": ["dm-akronsk", "dm-albany"],
        }
        ```

    Raises:
        ValueError: если переданы неизвестные или пустые параметры

    Returns:
        list[QueryParam]: список кортежей из переданных параметров + brief и limit:
        ```python
        [
            ("manufacturer_id", 3),
            ("role", "router"),
            ("status", "active"),
            ("status", "offline"),
            ("site_id", 2),
            ("site_id", 3),
            ("brief", "true"),
            ("limit", 500),
        ]
        ```
    """
    if len(request_params) == 0:
        raise ValueError("отсутствуют параметры запроса")

    func_map: dict[str, Callable[[str], QueryParam]] = {
        "name": lambda item: ("name__ie", item.lower()),
        "site": lambda item: ("site_id", _get_site_id(item)),
        "role": lambda item: ("role_id", _get_device_role_id(item)),
        "manufacturer": lambda item: ("manufacturer_id", _get_manufacturer_id(item)),
        "status": lambda item: ("status", item),
    }
    query_param_list = []
    for item_type, items in request_params.items():
        func = func_map.get(item_type)
        if func is None:
            raise ValueError("неизвестный тип параметра")
        query_param_list.extend([func(item) for item in items])

    query_param_list.append(("brief", "true"))
    query_param_list.append(("limit", 500))
    return query_param_list


if __name__ == "__main__":
    result = craft_nb_query(EXAMPLE_INPUT)
    assert tuple(result) == EXAMPLE_RESULT, "функция 'craft_nb_query' работает некорректно"
    print(
        "{}{}{}".format(
            NETBOX_URL,
            "/api/dcim/devices/?",
            urlencode(result),
        ),
    )
