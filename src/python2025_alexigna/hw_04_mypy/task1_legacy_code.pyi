from collections.abc import Callable, Mapping
from typing import Sequence, TypeAlias

QueryParam: TypeAlias = tuple[str, str | int]

class NetboxObjectResolver:
    SITE_IDS: dict[str, int]
    ROLE_IDS: dict[str, int]
    MANUFACTURER_IDS: dict[str, int]
    @classmethod
    def get_site_id(cls, site_slug: str) -> QueryParam: ...
    @classmethod
    def get_role_id(cls, role_slug: str) -> QueryParam: ...
    @classmethod
    def get_manufacturer_id(cls, manufacturer_slug: str) -> QueryParam: ...
    @classmethod
    def get_name_ie(cls, name: int) -> QueryParam: ...
    @classmethod
    def get_status(cls, status: str) -> QueryParam: ...

def process_items(
    processor: Callable[[str], QueryParam],
    items: Sequence[str],
) -> Sequence[QueryParam]: ...
def craft_nb_query(
    request_params: Mapping[str, list[str]],
) -> Sequence[QueryParam]: ...
