import sys
from pathlib import Path
import argparse

# Ensure parent directory (project root) is on the import path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from utils.dedup_utils import detect_sha256_duplicates


def main():
    parser = argparse.ArgumentParser(
        description="Detect SHA256 duplicates in AndroZoo metadata CSV"
    )
    parser.add_argument(
        "-i", "--input",
        type=Path,
        default=project_root / "datasets" / "latest_with-added-date.csv.gz",
        help="Path to the gzipped metadata CSV file"
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=project_root / "results" / "duplicate_sha256s.txt",
        help="File to write duplicate SHA256 hashes"
    )
    parser.add_argument(
        "-c", "--chunksize",
        type=int,
        default=1_000_000,
        help="Number of rows per pandas chunk"
    )
    args = parser.parse_args()

    csv_path = args.input
    out_path = args.output

    print(f"Reading metadata CSV: {csv_path}")
    summary = detect_sha256_duplicates(csv_path, chunksize=args.chunksize)

    print(f"Total entries: {summary['total']}")
    print(f"Unique SHA256s: {summary['unique']}")
    print(f"Duplicate entries: {summary['duplicates']}")
    print(f"Duplicate percentage: {summary['percentage']:.2f}%")

    # Ensure output directory exists
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        for sha in summary["dupe_hashes"]:
            f.write(f"{sha}\n")
    print(f"Duplicate SHA256s written to {out_path}")


if __name__ == "__main__":
    main()
