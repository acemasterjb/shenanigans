from pprint import PrettyPrinter

import pandas as pd


pp = PrettyPrinter(2)


def get_spaces_dataframe(sanitized_spaces: list[dict]) -> pd.DataFrame:
    sanitized_spaces = [space for space in sanitized_spaces if space.get("space_id")]

    index = pd.Index(
        [space["space_id"] for space in sanitized_spaces],
        "str",
        name="Space ID",
        tupleize_cols=False,
    )

    return pd.DataFrame(sanitized_spaces, index=index)
