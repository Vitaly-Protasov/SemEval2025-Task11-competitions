#!/usr/bin/env python3

import csv
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

DATASET = "brighter-dataset/BRIGHTER-emotion-categories"
ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "official_test_data" / "brighter_emotion_categories" / "test"
README_PATH = ROOT / "official_test_data" / "brighter_emotion_categories" / "README.md"
ROW_BATCH_SIZE = 100
OUTPUT_COLUMNS = ["id", "text", "anger", "fear", "joy", "sadness", "surprise"]
LABEL_COLUMNS = {"anger", "fear", "joy", "sadness", "surprise"}


def get_json(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=120) as response:
        return json.load(response)


def info_url() -> str:
    query = urllib.parse.urlencode({"dataset": DATASET})
    return f"https://datasets-server.huggingface.co/info?{query}"


def rows_url(config: str, offset: int, length: int) -> str:
    query = urllib.parse.urlencode(
        {
            "dataset": DATASET,
            "config": config,
            "split": "test",
            "offset": offset,
            "length": length,
        }
    )
    return f"https://datasets-server.huggingface.co/rows?{query}"


def fetch_test_rows(config: str, total_rows: int) -> list[dict]:
    rows = []
    offset = 0

    while offset < total_rows:
        batch_size = min(ROW_BATCH_SIZE, total_rows - offset)
        payload = get_json(rows_url(config, offset, batch_size))
        batch = payload.get("rows", [])
        if not batch:
            raise RuntimeError(
                f"Received an empty batch for {config} at offset {offset}."
            )
        rows.extend(item["row"] for item in batch)
        offset += len(batch)
        time.sleep(0.05)

    if len(rows) != total_rows:
        raise RuntimeError(
            f"Expected {total_rows} rows for {config}, downloaded {len(rows)}."
        )

    return rows


def write_language_file(config: str, rows: list[dict]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / f"{config}.csv"
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        for row in rows:
            output_row = {}
            for column in OUTPUT_COLUMNS:
                value = row.get(column, "")
                if column in LABEL_COLUMNS and value is None:
                    value = 0
                output_row[column] = value
            writer.writerow(output_row)


def write_readme(configs: list[str]) -> None:
    README_PATH.parent.mkdir(parents=True, exist_ok=True)
    README_PATH.write_text(
        "\n".join(
            [
                "# Official BRIGHTER Test Data",
                "",
                "This folder was generated from the official Hugging Face dataset",
                "`brighter-dataset/BRIGHTER-emotion-categories`.",
                "",
                "Files in `test/` contain the test split for each official language",
                "configuration, exported as CSV with the Track A-style columns:",
                "`id,text,anger,fear,joy,sadness,surprise`.",
                "",
                "Notes:",
                "- The official dataset also contains a `disgust` label, which is not exported here.",
                "- If the API returns a missing value for one of the exported emotion columns,",
                "  this exporter normalizes it to `0`.",
                "- This data is kept separate from the Codabench reference set because the",
                "  official BRIGHTER IDs/language inventory do not align 1:1 with the current bundle.",
                "",
                "Generated configs:",
                ", ".join(configs),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    info = get_json(info_url())
    dataset_info = info.get("dataset_info", {})
    if not dataset_info:
        raise RuntimeError("Dataset info response did not contain any configurations.")

    configs = sorted(dataset_info.keys())
    for config in configs:
        split_info = dataset_info[config]["splits"]["test"]
        total_rows = split_info["num_examples"]
        rows = fetch_test_rows(config, total_rows)
        write_language_file(config, rows)
        print(f"Wrote {config}.csv with {total_rows} rows.")

    write_readme(configs)
    print(f"Finished writing official test data to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
