from typing import Any, Literal, overload


@overload
def api_request(method: Literal["POST"], url: str, data: dict[str, Any]) -> str: ...


@overload
def api_request(method: Literal["GET", "DELETE"], url: str) -> str: ...


def api_request(
    method: Literal["GET", "DELETE", "POST"],
    url: str,
    data: dict[str, Any] | None = None,
) -> str:
    if method == "POST":
        if data is None:
            raise ValueError("для метода POST, требуется указать аргумент data")
        return f"POST {url}, {data}"
    else:
        return f"{method} {url}"


if __name__ == "__main__":
    api_request("GET", "/user")
    api_request("POST", "/user", {"name": "admin"})
    api_request("POST", "/user")
    api_request("GET", "/user", {"name": "admin"})
