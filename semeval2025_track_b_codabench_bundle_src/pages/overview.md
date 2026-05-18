# SemEval 2025 Task 11 - Track B

Track B is the multilingual emotion intensity prediction track from SemEval 2025 Task 11, *Bridging the Gap in Text-Based Emotion Detection*.

Given a text snippet, systems predict the intensity of each perceived emotion on an ordinal scale from `0` to `3`.

The intensity classes are:

- `0`: No emotion
- `1`: Low degree of emotion
- `2`: Moderate degree of emotion
- `3`: High degree of emotion

This reproduced bundle evaluates the following intensity columns:

- `anger`
- `disgust` when present for the language
- `fear`
- `joy`
- `sadness`
- `surprise`

Some languages use six emotion columns, while others such as English use five and do not include `disgust`. Always follow the header shown in the corresponding public file for that language.

The supported Track B languages in this bundle are:

- Amharic
- Algerian Arabic
- Mandarin Chinese
- German
- English
- Spanish (Latin American)
- Hausa
- Portuguese (Brazilian)
- Romanian
- Russian
- Ukrainian

## What Participants Do

1. Download the public data from the competition page.
2. Train or adapt a model using the released `train` and `dev` files.
3. Generate one or more prediction files for the `test` split.
4. Zip the prediction files inside a folder named `track_b`.
5. Upload the zip file on Codabench.

## What The Platform Shows

Each submission is evaluated automatically. Codabench then shows:

- leaderboard scores for the overall average Pearson correlation and per-language averages
- a Visualization tab with a language-by-language breakdown
- a detailed results panel for the submitted languages

## About This Reproduction

This competition is a reproduction of the closed SemEval 2025 Track B Codabench competition, adapted to run as a self-contained Codabench bundle.
