# SemEval 2025 Task 11 Competitions

This repository contains the Codabench bundle source code for the following competitions:
1) **Track A competition**
- Source code: [semeval2025_track_a_codabench_bundle_src](./semeval2025_track_a_codabench_bundle_src)
- Codabench link: `https://www.codabench.org/competitions/16415/`
- Bundle: [semeval2025_track_a_codabench_bundle_src/bundle.zip](./semeval2025_track_a_codabench_bundle_src/bundle.zip)
- Public data in this bundle includes `train`, `dev`, and `test`.
- Track A therefore has released labeled training data.

2) **Track B competition**
- Source code: [semeval2025_track_b_codabench_bundle_src](./semeval2025_track_b_codabench_bundle_src)
- Codabench link: `https://www.codabench.org/competitions/16424/`
- Bundle: [semeval2025_track_b_codabench_bundle_src/bundle.zip](./semeval2025_track_b_codabench_bundle_src/bundle.zip)
- Public data in this bundle includes `train`, `dev`, and `test`.
- Track B therefore also has released labeled training data.
- Track B is slightly uneven across languages: not every language has every split in the original released data.

3) **Track C competition**
- Source code: [semeval2025_track_c_codabench_bundle_src](./semeval2025_track_c_codabench_bundle_src)
- Original Codabench link: `https://www.codabench.org/competitions/4892/`
- Bundle: [semeval2025_track_c_codabench_bundle_src/bundle.zip](./semeval2025_track_c_codabench_bundle_src/bundle.zip)
- Public data in this bundle includes only `dev` and `test`.
- Track C does not provide released training data in this reproduction.

## Rebuild The Bundles

Each task has its own rebuild script.

### Track A

Run:

```bash
python3 semeval2025_track_a_codabench_bundle_src/build_bundle.py
```

This rebuilds the Track A resource archives and the final Track A `bundle.zip`.

### Track B

Run:

```bash
python3 semeval2025_track_b_codabench_bundle_src/build_bundle.py
```

This rebuilds the Track B resource archives and the final Track B `bundle.zip`.

### Track C

Run:

```bash
python3 semeval2025_track_c_codabench_bundle_src/build_bundle.py
```

This rebuilds the Track C resource archives and the final Track C `bundle.zip`.

## Notes

- The rebuild script uses Python's built-in `zipfile` module and does not depend on the system `zip` command.
- The Track A bundle source tree lives under `semeval2025_track_a_codabench_bundle_src/`.
- The Track B bundle source tree lives under `semeval2025_track_b_codabench_bundle_src/`.
- The Track C bundle source tree lives under `semeval2025_track_c_codabench_bundle_src/`.
- If you change scoring, pages, public data, reference data, or the starting kit, rerun the corresponding rebuild script before uploading a new bundle.
