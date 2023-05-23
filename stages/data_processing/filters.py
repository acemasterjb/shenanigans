from typing import Any

import pandas as pd


def has_similar_names(space: pd.Series, subject_name: str) -> bool:
    positive_cases = [subject_name, subject_name.lower(), subject_name.upper()]

    space_name = space["space_name"]
    return any([case in space_name for case in positive_cases])


def has_comanality_in_strategies(
    space: pd.Series, subject_strategies: list[dict[str]]
) -> bool:
    for strategy in space["space_strategies"]:
        address = strategy["address"]
        for subject_strategy in subject_strategies:
            if address == subject_strategy["address"]:
                return True
    return False


def get_nonsense_daos_by_token_df(
    spaces_df: pd.DataFrame, subject: dict[str, Any]
) -> pd.DataFrame:
    subject_strategies = subject["space_strategies"]
    mask = spaces_df.apply(
        has_comanality_in_strategies, args=(subject_strategies,), axis=1
    )

    return spaces_df.loc[mask]


def get_nonsense_daos_by_space_name_df(
    spaces_df: pd.DataFrame, subject: dict[str, Any]
) -> pd.DataFrame:
    subject_space_name = subject["space_name"]

    mask = spaces_df.apply(has_similar_names, args=(subject_space_name,), axis=1)

    return spaces_df.loc[mask]


def find_dao(
    user_dao_name: str, dao_metadata_list: list[dict[str, dict]]
) -> dict | None:
    for dao_metadata in dao_metadata_list:
        api_dao_name = dao_metadata["daoName"]
        positive_cases: list[str] = [
            api_dao_name,
            api_dao_name.lower(),
            api_dao_name.upper(),
        ]

        if user_dao_name in positive_cases:
            return dao_metadata
    return None
