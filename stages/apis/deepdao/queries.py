from json import JSONDecodeError
from typing import Any

from httpx import AsyncClient, Client, Response, Timeout

from .deep_dao_headers import headers


TIMEOUT = Timeout(10.0, connect=30.0, read=30.0)


def try_to_get_json_from_resp(
    response: Response, key: str, default: list[dict] | dict
) -> dict[str, Any]:
    try:
        return response.json()[key]
    except (JSONDecodeError, KeyError):
        return default


def get_raw_dao_list(limit: int) -> list[dict]:
    url = f"https://deepdao-server.deepdao.io/dashboard/ksdf3ksa-937slj3?limit={limit}&offset=0&orderBy=totalValueUSD&order=DESC"

    with Client(headers=headers, timeout=TIMEOUT) as client:
        resp = client.get(url)
        return try_to_get_json_from_resp(resp, "daosSummary", [dict()])


async def get_raw_token_metadata(organization_id: str) -> dict[str, str]:
    url = f"https://deepdao-server.deepdao.io/discussion/{organization_id}/projectToken"

    async with AsyncClient(headers=headers, timeout=TIMEOUT) as client:
        resp = await client.get(url)
        return try_to_get_json_from_resp(resp, "data", dict())


async def get_raw_organization_data(organization_id: str) -> dict[str, Any]:
    url = f"https://deepdao-server.deepdao.io/organization/ksdf3ksa-937slj3/{organization_id}"

    async with AsyncClient(headers=headers, timeout=TIMEOUT) as client:
        resp = await client.get(url)
        return try_to_get_json_from_resp(resp, "data", dict())


def get_raw_dao_data(organization_id: str) -> list[dict]:
    url = f"https://deepdao-server.deepdao.io/organization/ksdf3ksa-937slj3/{organization_id}/dao"

    with Client(headers=headers, timeout=TIMEOUT) as client:
        resp = client.get(url)

        return try_to_get_json_from_resp(resp, "data", [dict()])


def get_raw_top_holders(organization_id: str) -> list[dict]:
    url = f"https://deepdao-server.deepdao.io/organization/ksdf3ksa-937slj3/{organization_id}/top-shareholders"

    with Client(headers=headers, timeout=TIMEOUT) as client:
        resp = client.get(url)
        return try_to_get_json_from_resp(resp, "shareholders", [dict()])
