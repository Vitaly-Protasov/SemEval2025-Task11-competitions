#!/usr/bin/env python3

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parent


def write_zip(zip_path: Path, base_dir: Path, members: list[Path]) -> None:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    if zip_path.exists():
        zip_path.unlink()

    with ZipFile(zip_path, "w", ZIP_DEFLATED) as archive:
        for member in members:
            member_path = base_dir / member
            if not member_path.exists():
                raise FileNotFoundError(f"Missing required path: {member_path}")

            if member_path.is_file():
                archive.write(member_path, member_path.relative_to(base_dir))
                continue

            for path in sorted(member_path.rglob("*")):
                if path.is_file():
                    archive.write(path, path.relative_to(base_dir))


def main() -> None:
    resources_dir = ROOT / "resources"
    write_zip(
        resources_dir / "track_c_public_data.zip",
        ROOT / "public_data",
        [Path("track_c")],
    )
    write_zip(
        resources_dir / "track_c_reference_data.zip",
        ROOT / "build" / "reference_data",
        [Path(".")],
    )
    write_zip(
        resources_dir / "track_c_scoring_program.zip",
        ROOT / "build" / "scoring_program",
        [Path(".")],
    )
    write_zip(
        resources_dir / "track_c_ingestion_program.zip",
        ROOT / "build" / "ingestion_program",
        [Path(".")],
    )
    write_zip(
        resources_dir / "track_c_zero_submission.zip",
        ROOT / "starting_kit" / "sample_submission",
        [Path("track_c")],
    )
    write_zip(
        ROOT / "starting_kit" / "track_c_zero_submission.zip",
        ROOT / "starting_kit" / "sample_submission",
        [Path("track_c")],
    )
    write_zip(
        ROOT / "bundle.zip",
        ROOT,
        [
            Path("competition.yaml"),
            Path("images"),
            Path("pages"),
            Path("resources"),
            Path("starting_kit"),
        ],
    )
    print(ROOT / "bundle.zip")


if __name__ == "__main__":
    main()
