from numpy import concatenate

from stages import (
    get_nonsense_dao_data,
    get_raw_nonsense_proposals,
)
from stages.dataframes import (
    export_vote_data_to_csv,
    get_complete_vote_data_df,
    get_complete_vote_data_dfs,
    get_nonsense_dao_proposals_dfs,
)


if __name__ == "__main__":
    space_id_whitelist = ["aave.eth", "aavegotchi.eth", "butteryaave.eth"]
    nonsense_daos_df, subject_space_proposal_data = get_nonsense_dao_data(
        "aave.eth", "0xf6da417983653f7e7f5560a8e16ad77d5e25533bba9157abfd222347b40d09d0"
    )
    subject_vote_data_df = get_complete_vote_data_df(
        "Aave",
        subject_space_proposal_data["votes"],
        proposal=subject_space_proposal_data,
    )

    nonsense_daos_df = nonsense_daos_df.drop(space_id_whitelist, axis=0)

    raw_nonsense_proposals = get_raw_nonsense_proposals(nonsense_daos_df)

    nonsense_proposals_votes = {
        space_name: list(
            concatenate([proposal["votes"] for proposal in proposals]).flat
        )
        for space_name, proposals in raw_nonsense_proposals.items()
    }

    nonsense_daos_proposal_dfs = get_nonsense_dao_proposals_dfs(raw_nonsense_proposals)
    complete_vote_data_dfs = get_complete_vote_data_dfs(
        nonsense_proposals_votes, nonsense_daos_proposal_dfs
    )

    export_vote_data_to_csv(complete_vote_data_dfs)
    export_vote_data_to_csv({"Aave": subject_vote_data_df}, "_subject")
