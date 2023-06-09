from typing import Any

from .apis.deepdao.adapters import (
    get_snapshot_id,
)
from .apis.deepdao.queries import (
    get_raw_dao_data,
    get_raw_dao_list,
)
from .apis.dune.queries import get_raw_space_list
from .apis.snapshot.execution import get_proposals, get_space, get_votes
from .data_processing.filters import find_dao


async def get_all_proposals(
    nonsense_spaces: list[tuple[str, str]]
) -> dict[str, list[dict]]:
    all_spaces_proposals = dict()

    for space_id, space_name in nonsense_spaces:
        print(f"Getting vote data for {space_name}...")
        space_proposals: list[dict] = [
            proposal
            | await get_votes(proposal.get("id", ""))
            | {"space_id": space_id, "space_name": space_name}
            async for proposal in get_proposals(space_id)
        ]

        all_spaces_proposals[space_name] = space_proposals

    return all_spaces_proposals


def get_governance_strategy(raw_strategy: dict[str, Any]):
    if "governanceStrategy" in raw_strategy["params"]:
        return {
            "type": "governanceStrategy",
            "address": raw_strategy["params"]["governanceStrategy"],
            "network": raw_strategy["network"],
        }
    else:
        return dict()


def get_strategies(raw_strategies: list[dict[str, Any]]) -> list[str]:
    strategies = []
    for raw_strategy in raw_strategies:
        maybe_params: dict[str, Any] = raw_strategy.get("params")
        if not maybe_params:
            continue
        payload = dict()

        if not maybe_params.get("address"):
            if raw_strategy["name"] == "multichain":
                strategies.extend(get_strategies(maybe_params["strategies"]))
                continue
            else:
                payload.update(get_governance_strategy(raw_strategy))
                if not payload:
                    continue
        else:
            payload.update(
                {
                    "type": raw_strategy["name"],
                    "address": maybe_params["address"],
                    "network": raw_strategy["network"],
                }
            )

        strategies.append(payload)
    return strategies


def sanitize_space(space: dict):
    temp_space = dict()

    maybe_space_id = space.get("id")
    if not maybe_space_id:
        return None
    temp_space["space_id"] = maybe_space_id
    temp_space["space_name"] = space["name"]
    temp_space["space_network"] = space["network"]
    temp_space["space_domain"] = space["domain"]
    temp_space["space_strategies"] = get_strategies(space["strategies"])

    space.clear()
    space |= temp_space

    return space


async def get_dao_metadata(raw_dao: dict) -> dict[str, Any]:
    raw_dao_id = raw_dao.get("organizationId")
    raw_dao_data = get_raw_dao_data(raw_dao_id)
    dao_snapshot_id = get_snapshot_id(raw_dao_data)

    return dao_snapshot_id


async def get_single_dao_snapshot(raw_dao: dict) -> dict[str, dict] | None:
    print(f"Getting raw snapshot data for {raw_dao['daoName']}")
    dao_metadata = await get_dao_metadata(raw_dao)
    dao_snapshot_id = dao_metadata
    if not dao_snapshot_id:
        return None

    raw_space: dict[str, Any] = (await get_space(dao_snapshot_id))["space"]
    if not raw_space:
        return None

    raw_space = sanitize_space(raw_space.copy())
    print("\tDone getting space")
    return raw_space


async def dao_snapshot_data() -> list[dict]:
    raw_spaces: list[dict] = get_raw_space_list()["rows"]
    spaces = []

    for i, raw_space in enumerate(raw_spaces.copy()):
        try:
            complete_raw_space = (await get_space(raw_space["id"]))["space"]
            print(f"Sanitizing space data for {complete_raw_space.get('name')}")
            complete_raw_space = sanitize_space(complete_raw_space.copy())
            if complete_raw_space:
                spaces.append(complete_raw_space)
        except TypeError:  # bad api response object
            del raw_spaces[i]
            continue

    return spaces


async def dao_snapshot_data_for(
    dao_name: str, list_cutoff: int = 100
) -> dict[str, dict]:
    raw_daos = get_raw_dao_list(list_cutoff)
    raw_dao = find_dao(dao_name, raw_daos)

    if not raw_dao:
        return dict()

    return await get_single_dao_snapshot(raw_dao)
