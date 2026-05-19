# Data

The public data download contains:

- `track_c/dev/*.csv`: labeled development data
- `track_c/test/*.csv`: evaluation texts with blank label columns

Track C does **not** include a released `train` split in this bundle.
This means Track C does **not** provide released public training data to participants.

Use `dev` as the labeled source data for cross-lingual modeling. Use `test` only to build the final prediction files that you upload to Codabench.

Each `test` file contains:

- the instance `id`
- the input `text`
- blank label columns to show the required prediction header

Submit one or more CSV files named `pred_<lang>.csv`. Each file must contain the same IDs as the corresponding `test` file, in any row order, with an `id` column followed by the label columns shown in the test header.

Example:

```csv
id,anger,fear,joy,sadness,surprise
eng_test_track_c_00001,0,1,0,0,1
```

Example for a language with `disgust` and without `surprise`:

```csv
id,anger,disgust,fear,joy,sadness
afr_test_track_c_00001,0,0,0,1,0
```

Recommended submission layout:

```text
track_c/
  pred_eng.csv
  pred_deu.csv
  pred_hau.csv
```

You may submit predictions for a single language or for multiple languages in the same zip file.

Use the IDs from the Track C `test` files when preparing a submission. Files built from `dev` IDs will be rejected, because evaluation is performed against the `test` IDs for each language.

See the Submission Instructions page for the full upload procedure and folder layout.
