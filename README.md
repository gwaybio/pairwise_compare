[![Tests](https://github.com/WayScience/pairwise_compare/actions/workflows/python-app.yml/badge.svg)](https://github.com/WayScience/pairwise_compare/actions/workflows/python-app.yml)
# Pairwise Compare
Compare the rows of a [tidy](https://tidyr.tidyverse.org/articles/tidy-data.html) pandas dataframe in pairs, for example the correlation between the profiles of wells that differ in their cell line.
You choose which columns must be different and which must be the same between the two rows of a pair, and get one result per pair.

The [example notebook](docs/example_pairwise_comparisons.ipynb) uses a dataset from the [nf1_schwann_cell_painting_data](https://github.com/WayScience/nf1_schwann_cell_painting_data).
Most of the development is in the `src` folder.

## Installation
For Python 3.10 or newer, install the package with either of the following commands:<br>
`pip install pairwise-compare`<br>
`uv add pairwise-compare`

## Quick start
```python
from pairwise_compare import compare_pairs

results = compare_pairs(
    df,                                        # one row per well, with metadata and feature columns
    different=["Metadata_siRNA", "Metadata_Well"],  # the two rows of a pair differ in all of these
    features=feature_columns,                  # the numeric columns to compare
    same=["Metadata_Concentration"],           # and match in all of these (optional)
)
```
The result has one row per pair of rows, with their Pearson correlation across the features:

| pearsons_correlation | Metadata_Concentration__group0 | Metadata_Concentration__group1 | Metadata_siRNA__group0 | Metadata_siRNA__group1 | Metadata_Well__group0 | Metadata_Well__group1 |
| --- | --- | --- | --- | --- | --- | --- |
| 0.91 | 1.0 | 1.0 | siRNA A | siRNA B | A1 | B2 |

## Which rows are compared
- Two rows are compared when they have a different value in **every** `different` column and, if `same` is given, the same value in **every** `same` column.
- `different` needs at least two columns, or one column and at least one `same` column. A column cannot be in both.
- Each pair is compared once: the pair (A, B) is not repeated as (B, A), and a row is not compared with itself.
- `group0` and `group1` in the output are the two rows of a pair. For a `same` column both have the same value.
- `drop` leaves columns of `same` or `different` out of the results. They still decide which rows are compared. For example, `drop=["Metadata_Well"]` removes the well columns and keeps the others.

## Missing values
- A row with a missing value in a `same` or `different` column is **left out** of the comparisons, with a warning that says how many rows and which columns.
- A row with a missing value in a feature column is kept, and the results of its comparisons are missing (NaN), with a warning.
- Missing values in other columns are ignored.
- A row with the same value in every feature has no Pearson correlation (NaN), with a warning.

## Other comparisons
`compare_pairs` uses the Pearson correlation by default. To compare the rows another way, pass a comparator, which is a class that inherits from `Comparator` (see [Comparator.py](src/pairwise_compare/comparators/Comparator.py) and the example in [test_comparator.py](tests/test_comparator.py)):
- `__call__(group0, group1)` compares the feature values of two groups of rows and saves the results.
- `save_groups(group_columns, **groups)` saves the values of the group columns of the two groups.

A comparator keeps the results of every comparison it has made, so use a new one for each call to `compare_pairs`.

## Development
Install the package with its test dependencies and run the tests with [uv](https://docs.astral.sh/uv/):<br>
`uv sync`<br>
`uv run pytest --cov`

The version comes from the git tag of the release.
Release Drafter keeps a draft release with the notes of the merged pull requests (give a pull request the label `release-minor` or `release-major` to raise the version more than a patch).
To make a release, publish the draft on GitHub, which creates the tag and publishes the package to PyPI (see `.github/workflows/publish.yml`).
