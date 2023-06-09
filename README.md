# 🕵️ Governance Shenanigans

Investigating Snapshot spaces with questionable motives.

**Status**: WIP

## Dependencies

- Python >=3.10
- A way to manage the dependencies w/ a [pyproject.toml](./pyproject.toml) file (e.g. [rye](https://github.com/mitsuhiko/rye) or [poetry](https://github.com/python-poetry/poetry))

## Usage

```console
$ python main.py
```

This produces:

- a `nonsense_daos.csv` file in [`./data/`](./data/)
- multiple `*.csv` data files in [`./data/vote`](./data/vote)

The `nonsense_daos.csv` file contains metadata of Snapshot spaces that:

1. have the same token as a given subject (right now Aave is used as an example, you can change this in [main](./main.py#L142))
2. have the same/similar name as a given subject

The multiple `*.csv` files generated contain vote data of (up to) the last 150 proposals from daos listed in `nonsense_daos.csv`.