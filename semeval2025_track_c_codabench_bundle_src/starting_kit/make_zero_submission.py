#!/usr/bin/env python3
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PUBLIC_TEST = ROOT.parent / "public_data" / "track_c" / "test"
OUT = ROOT / "sample_submission" / "track_c"

OUT.mkdir(parents=True, exist_ok=True)
for path in sorted(PUBLIC_TEST.glob("*.csv")):
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        labels = [name for name in reader.fieldnames if name not in {"id", "text"}]
        rows = list(reader)
    with (OUT / f"pred_{path.stem}.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id"] + labels)
        writer.writeheader()
        for row in rows:
            writer.writerow({"id": row["id"], **{label: 0 for label in labels}})

print(f"Wrote {len(list(OUT.glob('*.csv')))} prediction files to {OUT}")
