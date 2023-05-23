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

A `nonsense_daos.csv` file will be generated within [data](./data/) filled with metadata of Snapshot spaces that:

1. have the same token as a given subject (right now Aave is used as an example, you can change this in [main](./main.py))
2. have the same/similar name as a given subject
