import click
from numpy import concatenate

from click_types import Blacklist
from docs import help
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


@click.command()
@click.option("-sid", "--space_id", help=help["space_id"])
@click.option("-pid", "--proposal_id", help=help["proposal_id"])
@click.option("-b", "--blacklist", type=Blacklist(), help=help["blacklist"])
def run(space_id: str, proposal_id: str, blacklist: list[str]):
    space_id_blacklist = blacklist if blacklist else []
    nonsense_daos_df, subject_space_proposal_data = get_nonsense_dao_data(
        space_id, proposal_id
    )

    nonsense_daos_df = nonsense_daos_df.drop(space_id_blacklist, axis=0)

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

    subject_space_name = subject_space_proposal_data["space_name"]
    subject_vote_data_df = get_complete_vote_data_df(
        subject_space_name,
        subject_space_proposal_data["votes"],
        proposal=subject_space_proposal_data,
    )

    export_vote_data_to_csv(complete_vote_data_dfs, "nonsense_spaces")
    export_vote_data_to_csv(
        {subject_space_name: subject_vote_data_df},
        f"{subject_space_name}_subject",
    )
