from asyncio import run as run_asyncio
from pprint import PrettyPrinter

import pandas as pd

from stages import dataframes, extract, export
from stages.data_processing import filters

pp = PrettyPrinter()

if __name__ == "__main__":
    subject = run_asyncio(extract.dao_snapshot_data_for("Aave"))
    spaces = run_asyncio(extract.dao_snapshot_data())

    spaces_df = (
        dataframes.get_spaces_dataframe(spaces)
        .drop_duplicates(["space_id"])
        .drop(["space_id"], axis=1)
    )
    nonsense_daos_df = filters.get_nonsense_daos_by_token_df(spaces_df, subject)
    nonsense_daos_df = pd.concat(
        [
            nonsense_daos_df,
            filters.get_nonsense_daos_by_space_name_df(spaces_df, subject),
        ]
    )

    export.dataframe_to_csv(nonsense_daos_df, "./data/nonsense_daos.csv")

    pp.pprint(nonsense_daos_df)
