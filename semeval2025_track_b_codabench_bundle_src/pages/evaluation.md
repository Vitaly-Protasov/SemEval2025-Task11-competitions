# Evaluation

Track B uses Pearson correlation, matching the shared-task evaluation setup for emotion intensity prediction.

For each submitted language:

- Pearson correlation is computed independently for each emotion column.
- The language score is the mean of these per-emotion Pearson correlations.

The set of evaluated emotion columns depends on the language-specific test file. Some languages include `disgust`, while others such as English do not.

The leaderboard reports:

- `avg_pearson_r`: mean per-language Pearson correlation over all supported test languages; languages omitted from the current submission contribute `0.0`
- `languages_scored`: number of languages included in the current submission
- one language-specific average Pearson correlation column per supported language

Submissions may contain any subset of supported languages. Missing languages are not treated as an error; their language-specific leaderboard cells remain empty for that submission, but they count as `0.0` in the global average.

## Detailed Results And Visualization

For each successful submission, Codabench also shows:

- a submission-level detailed results panel
- a Visualization tab with one section per submitted language

The visualization displays:

- the full language name
- one row per emotion column
- the Pearson correlation for each emotion
- the language-level average Pearson correlation

This view is intended to make it easy to compare emotion-specific intensity performance across languages.

Validation checks:

- file names must follow `pred_<lang>.csv`
- each submitted language must be supported by Track B
- headers must match the corresponding gold label file
- IDs must exactly match the evaluation set for that language
- predictions must be integers in the range `0` to `3`

## Participation Workflow

The expected workflow is:

1. Download the public data.
2. Train and validate on `train` and `dev`.
3. Build prediction files from the released `test` files.
4. Zip the `track_b` folder and upload it.
5. Review the leaderboard, detailed results, and visualization output.
