# Submission Instructions

You must submit one or more prediction files in `.csv` format. Each prediction file must be named:

`pred_<lang_code>.csv`

For example:

- `pred_eng.csv`
- `pred_hau.csv`
- `pred_ptbr.csv`

## File Format

Each file must contain:

- an `id` column
- the emotion columns in the same order as the corresponding public `test` file
- one row for every test instance of that language

Example:

```csv
id,anger,fear,joy,sadness,surprise
eng_test_track1_001,0,0,1,0,0
eng_test_track1_002,1,0,0,0,0
eng_test_track1_003,0,1,0,1,0
```

Important:

- the IDs must come from the released `track_a/test/<lang>.csv` file
- the header must match the corresponding `test` file
- prediction values must be binary: `0` or `1`

## Naming And Folder Layout

When uploading predictions on Codabench:

1. Choose the language or languages you want to submit.
2. Create a folder named `track_a`.
3. Put each prediction file inside that folder.
4. Zip the folder.
5. Upload the zip file on the submission page.

Example layout:

```text
track_a/
  pred_eng.csv
  pred_deu.csv
  pred_hau.csv
```

The scorer accepts any subset of supported languages, as long as the file names follow the required pattern.

## Single-Language Submission

To submit for one language only:

1. Create `track_a/`
2. Put one file inside it, for example `pred_hau.csv`
3. Zip the `track_a` folder
4. Upload the zip file on Codabench

## Multi-Language Submission

To submit for multiple languages:

1. Create `track_a/`
2. Put multiple prediction files inside it
3. Zip the `track_a` folder
4. Upload the zip file on Codabench

Example:

```text
track_a/
  pred_afr.csv
  pred_deu.csv
  pred_eng.csv
  pred_esp.csv
  pred_hin.csv
  pred_mar.csv
  pred_ptbr.csv
  pred_rus.csv
  pred_sun.csv
  pred_tat.csv
```

## Validation Rules

Each uploaded submission is checked automatically.

A submission will fail validation if:

- a file name does not follow `pred_<lang>.csv`
- a language is not supported by this bundle
- the header does not match the corresponding test file
- a file uses `dev` IDs instead of `test` IDs
- rows are missing or extra
- any prediction value is not `0` or `1`

## Practical Tips

- Always generate predictions from the released `test` files, not from `dev`.
- Keep one prediction file per language.
- Before uploading, open the zip and confirm that `track_a/` is at the zip root.
- If you want a language to receive a per-language score, include its prediction file in the submission.
