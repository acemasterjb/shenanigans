from asyncio import run as run_asyncio
from os.path import exists
from typing import Any

import pandas as pd

from . import dataframes, extract, export
from .data_processing import filters


def export_vote_data_to_csv(complete_vote_data_dfs: dict[str, pd.DataFrame]):
    for space_name, space_vote_data_df in complete_vote_data_dfs.items():
        print(f"generating csv for {space_name}...")
        space_vote_data_df.to_csv("./data/vote/" + space_name + ".csv", chunksize=50)


def get_complete_vote_data_df(
    space_name: str,
    space_votes: list,
    nonsense_daos_proposal_dfs: dict[str, pd.DataFrame],
) -> pd.DataFrame:
    num_rows = len(space_votes)
    nonsense_daos_vote_df = pd.DataFrame(
        space_votes,
        index=[vote["id"] for vote in space_votes],
    )

    nonsense_daos_vote_df: pd.DataFrame = nonsense_daos_vote_df
    if nonsense_daos_vote_df.empty:
        return pd.DataFrame()
    first_row = nonsense_daos_vote_df.iloc[0]
    nonsense_daos_vote_df["proposal_id"] = first_row["proposal"]["id"]

    nonsense_daos_vote_df = nonsense_daos_vote_df.drop(["proposal"], axis=1)
    nonsense_dao_proposals = nonsense_daos_proposal_dfs[space_name]
    proposal_id = nonsense_daos_vote_df.iloc[0]["proposal_id"]
    proposal: pd.Series = nonsense_dao_proposals.loc[proposal_id]

    nonsense_daos_vote_df["proposal_id"] = proposal["id"]
    nonsense_daos_vote_df["proposal_author"] = proposal["author"]
    nonsense_daos_vote_df["proposal_created"] = proposal["created"]
    nonsense_daos_vote_df["proposal_network"] = proposal["network"]
    nonsense_daos_vote_df["proposal_type"] = proposal["type"]
    nonsense_daos_vote_df["proposal_title"] = proposal["title"]
    nonsense_daos_vote_df["proposal_choices"] = [
        proposal["choices"] for _ in range(num_rows)
    ]
    nonsense_daos_vote_df["proposal_start"] = proposal["start"]
    nonsense_daos_vote_df["proposal_end"] = proposal["end"]
    nonsense_daos_vote_df["proposal_quorum"] = proposal["quorum"]
    nonsense_daos_vote_df["proposal_state"] = proposal["state"]
    nonsense_daos_vote_df["proposal_scores"] = [
        proposal["scores"] for _ in range(num_rows)
    ]
    nonsense_daos_vote_df["proposal_scores_total"] = proposal["scores_total"]
    nonsense_daos_vote_df["space_id"] = proposal["space_id"]
    nonsense_daos_vote_df["space_name"] = proposal["space_name"]

    return nonsense_daos_vote_df


def get_complete_vote_data_dfs(
    nonsense_proposals_votes: dict[str, list],
    nonsense_daos_proposal_dfs: dict[str, pd.DataFrame],
) -> dict[str, pd.DataFrame]:
    nonsense_daos_vote_dfs = dict()
    for space_name, space_votes in nonsense_proposals_votes.items():
        maybe_complete_vote_data_df = get_complete_vote_data_df(
            space_name, space_votes, nonsense_daos_proposal_dfs
        )
        if maybe_complete_vote_data_df.empty:
            print(f"\tno vote data for space {space_name}, continuing...")
            continue

        nonsense_daos_vote_dfs[space_name] = maybe_complete_vote_data_df

    return nonsense_daos_vote_dfs


def get_nonsense_dao_proposals_dfs(
    raw_nonsense_proposals: dict[str, list[dict]]
) -> dict[str, pd.DataFrame]:
    def remove_and_return(proposal: dict[str, Any]):
        proposal.pop("votes")
        return proposal

    nonsense_daos_proposals = {
        space_name: [
            remove_and_return(proposal) for proposal in proposals if proposal.get("id")
        ]
        for space_name, proposals in raw_nonsense_proposals.items()
    }

    return {
        space_name: pd.DataFrame(
            space_proposals,
            index=[proposal["id"] for proposal in space_proposals],
        )
        for space_name, space_proposals in nonsense_daos_proposals.items()
    }


def get_raw_nonsense_proposals(nonsense_daos_df: pd.DataFrame) -> dict[str, list[dict]]:
    nonsense_space_metadatas: list[tuple[str, str]] = [
        metadata for metadata in nonsense_daos_df["space_name"].items()
    ]

    return run_asyncio(extract.get_all_proposals(nonsense_space_metadatas))


def get_fresh_nonsense_dao_data(subject_dao_name: str) -> pd.DataFrame:
    subject = run_asyncio(extract.dao_snapshot_data_for(subject_dao_name))

    spaces = run_asyncio(extract.dao_snapshot_data())
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
    return nonsense_daos_df


def get_nonsense_dao_data(subject_dao_name: str) -> pd.DataFrame:
    if not exists("./data/nonsense_daos.csv"):
        return get_fresh_nonsense_dao_data(subject_dao_name)
    else:
        return pd.read_csv("./data/nonsense_daos.csv", index_col=0)
