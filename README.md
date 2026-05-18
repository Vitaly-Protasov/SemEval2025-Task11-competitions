# SemEval 2025 Task 11 Competitions

This repository contains the Codabench bundle source code for the following competitions:
1) **Track A competition:**
- Source code: [semeval2025_track_a_codabench_bundle_src](./semeval2025_track_a_codabench_bundle_src)
- Codebench link: https://www.codabench.org/competitions/16415/

## Rebuild The Bundle

To rebuild the internal resource archives and the top-level Codabench upload bundle, run:

```bash
python3 build_bundle/build_bundle.py
```

This rebuilds:

- `resources/track_a_public_data.zip`
- `resources/track_a_reference_data.zip`
- `resources/track_a_scoring_program.zip`
- `resources/track_a_ingestion_program.zip`
- `resources/track_a_zero_submission.zip`
- `starting_kit/track_a_zero_submission.zip`
- `bundle.zip`

The output bundle is:

- [bundle.zip](./semeval2025_track_a_codabench_bundle_src/bundle.zip)

## Notes

- The rebuild script uses Python's built-in `zipfile` module and does not depend on the system `zip` command.
- The active bundle source tree lives under `semeval2025_track_a_codabench_bundle_src/`.
- If you change scoring, pages, public data, reference data, or the starting kit, rerun the rebuild script before uploading a new bundle.
