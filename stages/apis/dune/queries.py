from json import JSONDecodeError
from os import environ
from typing import Any

from dotenv import load_dotenv
from httpx import Client, Response, Timeout


load_dotenv()
API_KEY = environ.get("DUNE_API")

HEADERS = {"x-dune-api-key": API_KEY}
TIMEOUT = Timeout(10.0, connect=30.0, read=30.0)


def try_to_get_json_from_resp(
    response: Response, key: str, default: list[dict] | dict, require_complete: bool
) -> dict[str, Any]:
    try:
        response_json = response.json()
        if require_complete and not (response_json["state"] == "QUERY_STATE_COMPLETED"):
            return default
        return response_json[key]
    except (JSONDecodeError, KeyError):
        return default


def get_raw_space_list(require_complete: bool = True) -> dict[str, Any]:
    url = f"https://api.dune.com/api/v1/query/2428726/results"

    with Client(headers=HEADERS, timeout=TIMEOUT) as client:
        resp = client.get(url)
        return try_to_get_json_from_resp(
            resp, "result", {"result": []}, require_complete
        )
