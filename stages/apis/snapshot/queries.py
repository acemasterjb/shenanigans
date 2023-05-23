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
