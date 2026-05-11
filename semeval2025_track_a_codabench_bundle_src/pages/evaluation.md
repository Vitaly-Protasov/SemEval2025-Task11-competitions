# Evaluation

Track A uses macro-F1 per language, matching the shared-task evaluation setup.

For each submitted language:

- F1 is computed independently for each emotion label.
- The language score is the mean of these per-label F1 values.

The leaderboard reports:

- `avg_macro_f1`: mean macro-F1 over all supported test languages. Languages omitted from the current submission contribute `0.0`.
- `avg_micro_f1`: mean micro-F1 over all supported test languages. Languages omitted from the current submission contribute `0.0`.
- `languages_scored`: number of languages included in the current submission.
- One language-specific macro-F1 column per supported language.

Submissions may contain any subset of supported languages. Missing languages are not treated as an error; their language-specific leaderboard cells remain empty for that submission, but they count as `0.0` in the global averages.

## Detailed Results And Visualization

For each successful submission, Codabench also shows:

- a submission-level detailed results panel
- a Visualization tab with one section per submitted language

The visualization displays:

- the full language name
- one row per emotion label
- the per-label F1 score
- the language-level average macro-F1

This view is intended to make it easy to compare emotion-specific performance across languages.

Validation checks:

- File names must follow `pred_<lang>.csv`.
- Each submitted language must be supported by Track A.
- Headers must match the corresponding gold label file.
- IDs must exactly match the evaluation set for that language.
- Predictions must be binary values, `0` or `1`.

## Participation Workflow

The expected workflow is:

1. Download the public data.
2. Train and validate on `train` and `dev`.
3. Build prediction files from the released `test` files.
4. Zip the `track_a` folder and upload it.
5. Review the leaderboard, detailed results, and visualization output.
