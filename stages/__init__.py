from asyncio import run as run_asyncio
from os.path import exists

import pandas as pd

from . import dataframes, extract, export
from .data_processing import filters


def get_raw_nonsense_proposals(nonsense_daos_df: pd.DataFrame) -> dict[str, list[dict]]:
    nonsense_space_metadatas: list[tuple[str, str]] = [
        metadata for metadata in nonsense_daos_df["space_name"].items()
    ]

    return run_asyncio(extract.get_all_proposals(nonsense_space_metadatas))


def get_fresh_nonsense_dao_data(
    subject_space_id: str, subject_proposal_id: str
) -> tuple[pd.DataFrame, dict]:
    subject, proposal_vote_data = run_asyncio(
        extract.get_full_snapshot_data_for(subject_space_id, subject_proposal_id)
    )

    spaces = run_asyncio(extract.get_snapshot_data())
    spaces_df = (
        dataframes.get_spaces_dataframe(spaces)
        .drop_duplicates(["space_id"])
        .drop(["space_id"], axis=1)
    )

    nonsense_daos_df = pd.concat(
        [
            filters.get_nonsense_daos_by_token_df(spaces_df, subject),
            filters.get_nonsense_daos_by_space_name_df(spaces_df, subject),
        ]
    )

    export.dataframe_to_csv(nonsense_daos_df, "./data/nonsense_daos.csv")
    return nonsense_daos_df, proposal_vote_data


def get_nonsense_dao_data(
    subject_space_id: str, subject_proposal_id: str
) -> tuple[pd.DataFrame, dict]:
    if not exists("./data/nonsense_daos.csv"):
        return get_fresh_nonsense_dao_data(subject_space_id, subject_proposal_id)
    else:
        _, proposal_vote_data = run_asyncio(
            extract.get_full_snapshot_data_for(subject_space_id, subject_proposal_id)
        )

        return pd.read_csv("./data/nonsense_daos.csv", index_col=0), proposal_vote_data
