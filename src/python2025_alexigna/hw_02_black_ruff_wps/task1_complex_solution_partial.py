from collections.abc import Callable, Mapping, Sequence
from functools import partial
from types import MappingProxyType
from typing import ClassVar, TypeAlias
from urllib.parse import urlencode

QueryParam: TypeAlias = tuple[str, str | int]

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


class NBQueryResolver:
    site_ids: ClassVar[dict[str, int]] = {
        "dm-akronsk": 2,
        "dm-albany": 3,
        "dm-binghamton": 4,
        "dm-buffalo": 5,
        "dm-camden": 6,
    }
    role_ids: ClassVar[dict[str, int]] = {
        "router": 1,
        "core-switch": 2,
        "distribution-switch": 3,
        "access-switch": 4,
    }
    manufacture_ids: ClassVar[dict[str, int]] = {
        "arista": 1,
        "cisco": 3,
        "juniper": 7,
    }

    @classmethod
    def get_site_id_param(cls, site_slug: str) -> QueryParam:
        site_id = cls.site_ids.get(site_slug)
        if site_id is None:
            msg = f"неизвестный сайт '{site_slug}'"
            raise ValueError(msg)
        return ("site_id", site_id)

    @classmethod
    def get_role_param(cls, role_slug: str) -> QueryParam:
        role_id = cls.role_ids.get(role_slug)
        if role_id is None:
            msg = f"неизвестная роль устройства '{role_slug}'"
            raise ValueError(msg)
        return ("role_id", role_id)

    @classmethod
    def get_manufacturer_param(cls, manufacturer_slug: str) -> QueryParam:
        manufacturer_id = cls.manufacture_ids.get(manufacturer_slug)
        if manufacturer_id is None:
            msg = f"неизвестный производитель '{manufacturer_slug}'"
            raise ValueError(msg)
        return ("manufacturer_id", manufacturer_id)

    @classmethod
    def get_name_ie_param(cls, name: str) -> QueryParam:
        return ("name_ie", name)

    @classmethod
    def get_status_param(cls, status: str) -> QueryParam:
        return ("status", status)


def processor(func: Callable[[str], QueryParam], items: Sequence[str]) -> list[QueryParam]:
    return [func(item) for item in items]


def craft_nb_query(request_params: Mapping[str, list[str]]) -> list[QueryParam]:
    """Преобразование набора параметров в request params.

    Args:
        request_params (dict[str, str]): параметры запроса.
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
        list[tuple[str, str | int]]: список кортежей из переданных параметров + brief и limit:
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

    query_param_list: list[QueryParam] = []
    func_map = {
        "name": partial(processor, NBQueryResolver.get_name_ie_param),
        "site": partial(processor, NBQueryResolver.get_site_id_param),
        "role": partial(processor, NBQueryResolver.get_role_param),
        "manufacturer": partial(processor, NBQueryResolver.get_manufacturer_param),
        "status": partial(processor, NBQueryResolver.get_status_param),
    }
    for item_type, items in request_params.items():
        func = func_map.get(item_type)
        if func is None:
            raise ValueError("неизвестный тип параметра")
        query_param_list.extend(func(items))

    query_param_list.extend(
        [
            ("brief", "true"),
            ("limit", 500),
        ],
    )
    return query_param_list


if __name__ == "__main__":
    result = craft_nb_query(EXAMPLE_INPUT)
    assert tuple(result) == EXAMPLE_RESULT, "функция 'craft_nb_query' работает некорректно"
    print(f"{NETBOX_URL}/api/dcim/devices/?{urlencode(result)}")
