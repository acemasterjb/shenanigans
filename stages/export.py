import pandas as pd


def dataframe_to_csv(
    shenanigan_dataframe: pd.DataFrame, file_name: str
):
    print("Generating csv...")
    shenanigan_dataframe.to_csv(
        file_name, chunksize=50
    )
    print("Done")
