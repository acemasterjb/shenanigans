# 🕵️ Governance Shenanigans

Investigating Snapshot spaces with questionable motives.

**Status**: WIP

## Dependencies

- Python >=3.10
- A way to manage dependencies using [pyproject.toml](./pyproject.toml) (e.g. [rye](https://github.com/mitsuhiko/rye) [preferred] or [poetry](https://github.com/python-poetry/poetry))

## Usage

```console
$ python main.py --help
Usage: main.py [OPTIONS]

Options:
  -sid, --space_id TEXT      Subject Space Snapshot id
  -pid, --proposal_id TEXT   Subject Snapshot Proposal id
  -b, --blacklist JSON_LIST  Omit these spaces from the set of nonsense spaces.
                             e.g. '["aave.eth", "aavegotchi.eth"]'
  --help                     Show this message and exit.
```

e.g.

``` console
$ python main.py -sid uniswap -pid <PROPOSAL_ID> -b '['SOME_TEST_SPACE', 'TEST_SPACE_2']'
```

This produces:

- a `nonsense_daos.csv` file in [`./data/`](./data/)
- multiple `*.csv` data files in [`./data/vote`](./data/vote)

The `nonsense_daos.csv` file contains metadata of Snapshot spaces that:

1. have the same token as a given subject
2. have the same/similar name as a given subject

The multiple `*.csv` files generated contain vote data of (up to) the last 150 proposals from daos listed in `nonsense_daos.csv`.
