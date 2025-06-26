from collections.abc import Callable, Mapping
from typing import Final, Sequence

type QueryParam = tuple[str, str | int]
type QueryParamProcessor = Callable[[str], QueryParam]

NETBOX_URL: Final[str]
EXAMPLE_INPUT: Mapping[str, list[str]]
EXAMPLE_RESULT: tuple[QueryParam, ...]

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
    def get_name_ie(cls, name: str) -> QueryParam: ...
    @classmethod
    def get_status(cls, status: str) -> QueryParam: ...

def processor(func: Callable[[str], QueryParam], items: Sequence[str]) -> list[QueryParam]: ...
def craft_nb_query(request_params: Mapping[str, list[str]]) -> Sequence[QueryParam]: ...
