#!/usr/bin/env python3
import os
import shutil
from pathlib import Path


def main():
    submission_dir = Path(os.environ.get("APP_INGESTED_PROGRAM", "/app/ingested_program"))
    output_dir = Path(os.environ.get("APP_OUTPUT", "/app/output"))
    output_dir.mkdir(parents=True, exist_ok=True)

    prediction_files = [
        path for path in submission_dir.rglob("pred_*.csv")
        if path.is_file() and "__MACOSX" not in path.parts and not path.name.startswith("._")
    ]

    if not prediction_files:
        raise SystemExit(
            "No prediction files named pred_<lang>.csv were found in the uploaded submission."
        )

    for path in prediction_files:
        destination = output_dir / path.name
        shutil.copy2(path, destination)

    print(f"Copied {len(prediction_files)} prediction files to {output_dir}")


if __name__ == "__main__":
    main()
