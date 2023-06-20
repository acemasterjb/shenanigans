import os
from typing import Any

import pandas as pd


def export_vote_data_to_csv(
    complete_vote_data_dfs: dict[str, pd.DataFrame], csv_name: str
):
    if os.path.exists(f"./data/vote/{csv_name}.csv.gzip"):
        os.remove(f"./data/vote/{csv_name}.csv.gzip")

    for space_name, space_vote_data_df in complete_vote_data_dfs.items():
        print(f"generating csv data for {space_name}...")
        space_vote_data_df.to_csv(
            f"./data/vote/{csv_name}.csv.gzip",
            mode="a+",
            compression="gzip",
            chunksize=50,
        )


def get_complete_vote_data_df(
    space_name: str,
    space_votes: list,
    nonsense_daos_proposal_dfs: dict[str, pd.DataFrame] = dict(),
    proposal: dict = dict(),
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
    if nonsense_daos_proposal_dfs:
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


def get_spaces_dataframe(sanitized_spaces: list[dict]) -> pd.DataFrame:
    sanitized_spaces = [space for space in sanitized_spaces if space.get("space_id")]

    index = pd.Index(
        [space["space_id"] for space in sanitized_spaces],
        "str",
        name="Space ID",
        tupleize_cols=False,
    )

    return pd.DataFrame(sanitized_spaces, index=index).drop_duplicates(["voter"])
