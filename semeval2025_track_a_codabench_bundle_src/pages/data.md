# Data

The public data download contains:

- `track_a/train/*.csv`: training data with labels.
- `track_a/dev/*.csv`: development data with labels.
- `track_a/test/*.csv`: evaluation texts with blank label columns.

This means Track A provides released labeled training data to participants.

Use `train` and `dev` for model development. Use `test` only to build the final prediction files that you upload to Codabench.

Each `test` file contains:

- the instance `id`
- the input `text`
- blank label columns to show the required prediction header

Submit one or more CSV files named `pred_<lang>.csv`. Each file must contain the same IDs as the corresponding `test` file, in any row order, with an `id` column followed by the emotion columns shown in the test header.

Example:

```csv
id,anger,fear,joy,sadness,surprise
deu_test_track_a_00001,0,0,0,0,0
```

Recommended submission layout:

```text
track_a/
  pred_eng.csv
  pred_deu.csv
  pred_hau.csv
```

You may submit predictions for a single language or for multiple languages in the same zip file.

Use the IDs from the Track A `test` files when preparing a submission. Files built from `dev` IDs will be rejected, because evaluation is performed against the `test` IDs for each language.

See the Submission Instructions page for the full upload procedure and folder layout.
