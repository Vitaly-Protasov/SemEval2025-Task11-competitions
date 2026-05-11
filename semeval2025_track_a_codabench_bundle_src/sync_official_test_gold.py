#!/usr/bin/env python3

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OFFICIAL_TEST = ROOT / "official_test_data" / "brighter_emotion_categories" / "test"
PUBLIC_TEST = ROOT / "public_data" / "track_a" / "test"
REFERENCE_DATA = ROOT / "build" / "reference_data"
SAMPLE_SUBMISSION = ROOT / "starting_kit" / "sample_submission" / "track_a"

SUPPORTED_LANGUAGES = [
    "afr", "arq", "ary", "chn", "deu", "eng", "esp", "hau", "hin", "ibo",
    "ind", "jav", "kin", "mar", "pcm", "ptbr", "ptmz", "ron", "rus", "sun",
    "swa", "swe", "tat", "ukr", "vmw", "xho", "yor", "zul",
]

LABELS = ["anger", "fear", "joy", "sadness", "surprise"]


def read_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def ensure_dirs() -> None:
    PUBLIC_TEST.mkdir(parents=True, exist_ok=True)
    REFERENCE_DATA.mkdir(parents=True, exist_ok=True)
    SAMPLE_SUBMISSION.mkdir(parents=True, exist_ok=True)


def remove_old_csvs(directory: Path) -> None:
    for path in directory.glob("*.csv"):
        path.unlink()


def write_public_test(language: str, rows: list[dict]) -> None:
    path = PUBLIC_TEST / f"{language}.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["id", "text"] + LABELS)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "id": row["id"],
                    "text": row["text"],
                    **{label: "" for label in LABELS},
                }
            )


def write_reference_data(language: str, rows: list[dict]) -> None:
    path = REFERENCE_DATA / f"{language}.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["id"] + LABELS)
        writer.writeheader()
        for row in rows:
            writer.writerow({"id": row["id"], **{label: row[label] for label in LABELS}})


def write_zero_submission(language: str, rows: list[dict]) -> None:
    path = SAMPLE_SUBMISSION / f"pred_{language}.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["id"] + LABELS)
        writer.writeheader()
        for row in rows:
            writer.writerow({"id": row["id"], **{label: 0 for label in LABELS}})


def main() -> None:
    ensure_dirs()
    remove_old_csvs(PUBLIC_TEST)
    remove_old_csvs(REFERENCE_DATA)
    remove_old_csvs(SAMPLE_SUBMISSION)

    for language in SUPPORTED_LANGUAGES:
        source = OFFICIAL_TEST / f"{language}.csv"
        if not source.exists():
            raise FileNotFoundError(f"Missing official test file: {source}")
        rows = read_rows(source)
        write_public_test(language, rows)
        write_reference_data(language, rows)
        write_zero_submission(language, rows)
        print(f"Synchronized {language}.csv with {len(rows)} rows.")


if __name__ == "__main__":
    main()
