from asyncio import sleep
from os import getenv
from typing import Any

from dotenv import load_dotenv
from gql import Client
from gql.transport.exceptions import TransportError, TransportServerError
from gql.transport.aiohttp import AIOHTTPTransport
from graphql import DocumentNode

from .queries import proposal, proposals, space, votes

load_dotenv()
transport = AIOHTTPTransport(
    url="https://hub.snapshot.org/graphql",
    headers={"x-api-key": getenv("SNAPSHOT_API"), "content-type": "application/json"},
)


async def try_result(query: DocumentNode) -> dict[str, list[dict]]:
    client = Client(transport=transport)
    session = await client.connect_async(reconnecting=True)

    try:
        result = await session.execute(query)
    except (TransportError, TransportServerError):
        await client.close_async()
        await sleep(21)
        return await try_result(client, query)
    finally:
        await client.close_async()

    return result


async def get_space(space_id: str) -> dict[str, dict[str, Any]]:
    query = space(space_id)
    result = await try_result(query)

    if not result["space"]:
        return {"space": dict()}
    return result


async def get_votes(
    proposal_id: str, limit: int = 1000, offset: int = 0
) -> dict[str, list[dict]]:
    default = {"votes": []}

    if not proposal_id:
        return default
    query = votes(proposal_id, limit, offset)
    result = await try_result(query)

    if not result["votes"]:
        return default

    if offset < 4999:
        if offset == 4000:
            offset -= 1
        result["votes"].extend(
            (await get_votes(proposal_id, offset=offset + limit)).copy()["votes"]
        )
    return result


async def get_proposal(proposal_id: str) -> dict[str, Any]:
    query = proposal(proposal_id)
    maybe_proposal = await try_result(query)
    if not maybe_proposal["proposal"]:
        return {"proposal": dict()}

    return maybe_proposal


async def get_proposals(
    space_id: str, limit: int = 150, offset: int = 0
) -> list[dict[str, Any]]:
    query = proposals(space_id, limit, offset)
    maybe_proposals = await try_result(query)
    if not maybe_proposals["proposals"]:
        yield dict()
    else:
        for result in maybe_proposals["proposals"]:
            yield result
