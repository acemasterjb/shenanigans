from graphql import DocumentNode
from gql import gql


def space(space_id: str) -> DocumentNode:
    query_params = """space(
        id: "{id}"
    )"""
    query_body = """{
        id
        name
        network
        domain
        strategies {
            name
            network
            params
        }
    }"""

    query_params = query_params.format(id=space_id)
    query = "".join(["query{", query_params, query_body, "}"])

    return gql(query)


def votes(proposal_id: str, limit: int = 1000, offset: int = 0) -> DocumentNode:
    query_params = """votes(
        first: {limit},
        skip: {offset},
        where: $1proposal: "{proposal_id}"$2
    )
    """

    query_body = """{
        id
        voter
        created
        proposal{
            id
        }
        choice
        metadata
        reason
        vp
        vp_by_strategy
    }
    """

    query_params = query_params.format(
        limit=limit, offset=offset, proposal_id=proposal_id
    )
    query_params = query_params.replace("$1", "{")
    query_params = query_params.replace("$2", "}")

    query = "".join(["query{", query_params, query_body, "}"])

    return gql(query)


proposal_query_body = """{
    id
    author
    created
    network
    type
    title
    choices
    start
    end
    quorum
    state
    scores
    scores_total
}
"""


def proposal(proposal_id: str):
    query_params = """proposal(
        id: "{proposal_id}"
    )
    """

    query_params = query_params.format(proposal_id=proposal_id)

    query = "".join(["query{", query_params, proposal_query_body, "}"])

    return gql(query)


def proposals(space_id: str, limit: int = 150, offset: int = 0) -> DocumentNode:
    query_params = """proposals(
        first: {limit},
        skip: {offset},
        where: $1space: "{space_id}"$2
    )
    """

    query_params = query_params.format(space_id=space_id, limit=limit, offset=offset)
    query_params = query_params.replace("$1", "{")
    query_params = query_params.replace("$2", "}")

    query = "".join(["query{", query_params, proposal_query_body, "}"])

    return gql(query)
