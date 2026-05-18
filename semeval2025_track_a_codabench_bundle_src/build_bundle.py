#!/usr/bin/env python3

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

REPO_ROOT = Path(__file__).resolve().parents[1]
BUNDLE_ROOT = REPO_ROOT / "semeval2025_track_a_codabench_bundle_src"

RESOURCES_DIR = BUNDLE_ROOT / "resources"
PUBLIC_DATA_DIR = BUNDLE_ROOT / "public_data"
REFERENCE_DATA_DIR = BUNDLE_ROOT / "build" / "reference_data"
SCORING_PROGRAM_DIR = BUNDLE_ROOT / "build" / "scoring_program"
INGESTION_PROGRAM_DIR = BUNDLE_ROOT / "build" / "ingestion_program"
STARTING_KIT_SAMPLE_DIR = BUNDLE_ROOT / "starting_kit" / "sample_submission"

PUBLIC_ZIP = RESOURCES_DIR / "track_a_public_data.zip"
REFERENCE_ZIP = RESOURCES_DIR / "track_a_reference_data.zip"
SCORING_ZIP = RESOURCES_DIR / "track_a_scoring_program.zip"
INGESTION_ZIP = RESOURCES_DIR / "track_a_ingestion_program.zip"
ZERO_SUBMISSION_ZIP = RESOURCES_DIR / "track_a_zero_submission.zip"
STARTING_KIT_ZERO_ZIP = BUNDLE_ROOT / "starting_kit" / "track_a_zero_submission.zip"
BUNDLE_ZIP = BUNDLE_ROOT / "bundle.zip"


def ensure_exists(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Missing required path: {path}")


def write_zip(zip_path: Path, base_dir: Path, members: list[Path]) -> None:
    ensure_exists(base_dir)
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    if zip_path.exists():
        zip_path.unlink()

    with ZipFile(zip_path, "w", ZIP_DEFLATED) as archive:
        for member in members:
            member_path = base_dir / member
            ensure_exists(member_path)

            if member_path.is_file():
                archive.write(member_path, member_path.relative_to(base_dir))
                continue

            for path in sorted(member_path.rglob("*")):
                if path.is_file():
                    archive.write(path, path.relative_to(base_dir))


def rebuild_bundle() -> None:
    write_zip(PUBLIC_ZIP, PUBLIC_DATA_DIR, [Path("track_a")])
    write_zip(REFERENCE_ZIP, REFERENCE_DATA_DIR, [Path(".")])
    write_zip(SCORING_ZIP, SCORING_PROGRAM_DIR, [Path(".")])
    write_zip(INGESTION_ZIP, INGESTION_PROGRAM_DIR, [Path(".")])
    write_zip(ZERO_SUBMISSION_ZIP, STARTING_KIT_SAMPLE_DIR, [Path("track_a")])
    write_zip(STARTING_KIT_ZERO_ZIP, STARTING_KIT_SAMPLE_DIR, [Path("track_a")])

    write_zip(
        BUNDLE_ZIP,
        BUNDLE_ROOT,
        [
            Path("competition.yaml"),
            Path("images"),
            Path("pages"),
            Path("resources"),
            Path("starting_kit"),
        ],
    )


def print_summary() -> None:
    outputs = [
        PUBLIC_ZIP,
        REFERENCE_ZIP,
        SCORING_ZIP,
        INGESTION_ZIP,
        ZERO_SUBMISSION_ZIP,
        STARTING_KIT_ZERO_ZIP,
        BUNDLE_ZIP,
    ]
    for path in outputs:
        print(f"{path.relative_to(REPO_ROOT)}: {path.stat().st_size:,} bytes")

    print()
    print(f"Bundle rebuilt at: {BUNDLE_ZIP}")


def main() -> None:
    rebuild_bundle()
    print_summary()


if __name__ == "__main__":
    main()
