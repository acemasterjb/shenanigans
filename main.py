from asyncio import run as run_asyncio
from os.path import exists
from pprint import PrettyPrinter

import pandas as pd

from stages import dataframes, extract, export
from stages.data_processing import filters

pp = PrettyPrinter()

if __name__ == "__main__":
    nonsense_daos_df = pd.DataFrame()

    if not exists("./data/nonsense_daos.csv"):
        subject = run_asyncio(extract.dao_snapshot_data_for("Aave"))

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
    else:
        nonsense_daos_df = pd.read_csv(
            "./data/nonsense_daos.csv",
            index_col=0,
        )

    space_id_whitelist = ["aave.eth", "aavegotchi.eth", "butteryaave.eth"]
    nonsense_daos_df = nonsense_daos_df.drop(space_id_whitelist, axis=0)

    pp.pprint(nonsense_daos_df)
