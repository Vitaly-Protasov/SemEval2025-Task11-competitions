#!/usr/bin/env python3

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_ROOT = Path(
    "/home/vitaly.protasov/competitions/semeval2025_task11_source/"
    "task-dataset/semeval-2025-task11-dataset/track_b"
)

PUBLIC_ROOT = ROOT / "public_data" / "track_b"
REFERENCE_ROOT = ROOT / "build" / "reference_data"
SAMPLE_ROOT = ROOT / "starting_kit" / "sample_submission" / "track_b"

SUPPORTED_LANGUAGES = [
    "amh",
    "arq",
    "chn",
    "deu",
    "eng",
    "esp",
    "hau",
    "ptbr",
    "ron",
    "rus",
    "ukr",
]


def read_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def clear_csvs(directory: Path) -> None:
    if not directory.exists():
        return
    for path in directory.glob("*.csv"):
        path.unlink()


def sync_public_split(split: str, language: str) -> None:
    src = SOURCE_ROOT / split / f"{language}.csv"
    if not src.exists():
        if split == "test":
            raise FileNotFoundError(f"Missing required Track B test file: {src}")
        return
    rows = read_rows(src)
    fieldnames = list(rows[0].keys()) if rows else []

    if split == "test":
        label_fields = [name for name in fieldnames if name not in {"id", "text"}]
        public_rows = []
        for row in rows:
            public_rows.append(
                {
                    "id": row["id"],
                    "text": row["text"],
                    **{label: "" for label in label_fields},
                }
            )
        write_csv(PUBLIC_ROOT / split / f"{language}.csv", fieldnames, public_rows)

        reference_rows = []
        for row in rows:
            reference_rows.append(
                {key: value for key, value in row.items() if key != "text"}
            )
        write_csv(
            REFERENCE_ROOT / f"{language}.csv",
            [name for name in fieldnames if name != "text"],
            reference_rows,
        )

        zero_rows = []
        label_fields = [name for name in fieldnames if name not in {"id", "text"}]
        for row in rows:
            zero_rows.append({"id": row["id"], **{label: 0 for label in label_fields}})
        write_csv(
            SAMPLE_ROOT / f"pred_{language}.csv", ["id"] + label_fields, zero_rows
        )
        return

    write_csv(PUBLIC_ROOT / split / f"{language}.csv", fieldnames, rows)


def main() -> None:
    for split in ["train", "dev", "test"]:
        clear_csvs(PUBLIC_ROOT / split)
    clear_csvs(REFERENCE_ROOT)
    clear_csvs(SAMPLE_ROOT)

    for language in SUPPORTED_LANGUAGES:
        for split in ["train", "dev", "test"]:
            sync_public_split(split, language)
        print(f"Synchronized Track B data for {language}.")


if __name__ == "__main__":
    main()
