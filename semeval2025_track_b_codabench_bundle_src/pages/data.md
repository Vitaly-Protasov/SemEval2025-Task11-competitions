# Data

The public data download contains:

- `track_b/train/*.csv`: training data with gold intensity labels
- `track_b/dev/*.csv`: development data with gold intensity labels
- `track_b/test/*.csv`: evaluation texts with blank intensity columns

This means Track B provides released labeled training data to participants.

Use `train` and `dev` for model development. Use `test` only to build the final prediction files that you upload to Codabench.

Important notes:

- available languages can vary by split
- some languages include `disgust`, while others do not
- the required prediction columns are exactly the columns shown in the corresponding public `test` file

Each `test` file contains:

- the instance `id`
- the input `text`
- blank intensity columns to show the required prediction header

Submit one or more CSV files named `pred_<lang>.csv`. Each file must contain the same IDs as the corresponding `test` file, in any row order, with an `id` column followed by the intensity columns shown in the test header.

Example:

```csv
id,anger,fear,joy,sadness,surprise
eng_test_track_b_00001,0,1,0,0,0
```

Example for a language with `disgust`:

```csv
id,anger,disgust,fear,joy,sadness,surprise
amh_test_track_b_00001,0,2,0,0,0,0
```

Recommended submission layout:

```text
track_b/
  pred_eng.csv
  pred_deu.csv
  pred_hau.csv
```

You may submit predictions for a single language or for multiple languages in the same zip file.

Use the IDs from the Track B `test` files when preparing a submission. Files built from `dev` IDs will be rejected, because evaluation is performed against the `test` IDs for each language.

See the Submission Instructions page for the full upload procedure and folder layout.
