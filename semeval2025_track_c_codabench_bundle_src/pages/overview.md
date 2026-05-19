# SemEval 2025 Task 11 - Track C

Track C is the multilingual cross-lingual emotion detection track from SemEval 2025 Task 11, *Bridging the Gap in Text-Based Emotion Detection*.

Given a labeled development set in one language, systems predict the perceived emotion labels of text instances in a different target language.

Labels are binary:

- `1` means the emotion is present
- `0` means the emotion is absent

This reproduced bundle evaluates the following emotion columns:

- `anger`
- `disgust` when present for the language
- `fear`
- `joy`
- `sadness`
- `surprise` when present for the language

Some languages use five emotion columns, while others use six. Always follow the header shown in the corresponding public file for that language.

The supported Track C languages in this bundle are:

- Afrikaans
- Amharic
- Algerian Arabic
- Moroccan Arabic
- Mandarin Chinese
- German
- English
- Spanish (Latin American)
- Hausa
- Hindi
- Igbo
- Indonesian
- Javanese
- Kinyarwanda
- Marathi
- Oromo
- Nigerian Pidgin
- Portuguese (Brazilian)
- Portuguese (Mozambican)
- Romanian
- Russian
- Somali
- Sundanese
- Swahili
- Swedish
- Tatar
- Tigrinya
- Ukrainian
- Emakhuwa
- isiXhosa
- Yoruba
- isiZulu

## Important Data Note

Track C does not provide a released training split in this bundle. Only:

- `dev` data with labels
- `test` data for evaluation

are included.

So unlike Track A and Track B, Track C does **not** include released public training data in this reproduction.

## What Participants Do

1. Download the public data from the competition page.
2. Use the released `dev` data as the labeled source data for cross-lingual experimentation.
3. Generate one or more prediction files for the `test` split.
4. Zip the prediction files inside a folder named `track_c`.
5. Upload the zip file on Codabench.

## What The Platform Shows

Each submission is evaluated automatically. Codabench then shows:

- leaderboard scores for the overall averages and per-language macro-F1 values
- a Visualization tab with a language-by-language breakdown
- a detailed results panel for the submitted languages

## About This Reproduction

This competition is a reproduction of the closed SemEval 2025 Track C Codabench competition, adapted to run as a self-contained Codabench bundle.
