from time import sleep
from typing import Any

from gql import dsl, Client
from gql.transport.exceptions import TransportError, TransportServerError
from gql.transport.aiohttp import AIOHTTPTransport
from graphql import DocumentNode

from .queries import space

transport = AIOHTTPTransport(url="https://hub.snapshot.org/graphql")
client = Client(transport=transport)


async def try_result(client: Client, query: DocumentNode) -> dict[str, list[dict]]:
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
    result = await try_result(client, query)

    if not result["space"]:
        return {"space": dict()}
    return result
