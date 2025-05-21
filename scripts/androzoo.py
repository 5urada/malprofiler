import sys
from pathlib import Path
import argparse

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from utils.dedup_utils import detect_hash_duplicates


def main():
    parser = argparse.ArgumentParser(
        description="Detect hash duplicates in AndroZoo metadata CSV"
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
        default=None,
        help="File to write duplicate hash values. If not set, uses results/duplicate_<hash>.txt"
    )
    parser.add_argument(
        "-c", "--chunksize",
        type=int,
        default=1_000_000,
        help="Number of rows per pandas chunk"
    )
    parser.add_argument(
        "-H", "--hash",
        type=str,
        default="sha256",
        choices=["sha256", "sha1", "md5"],
        help="Which hash column to deduplicate by"
    )
    args = parser.parse_args()

    csv_path = args.input
    hash_column = args.hash
    # Determine output path
    if args.output:
        out_path = args.output
    else:
        out_path = project_root / "results" / f"duplicate_{hash_column}.txt"

    print(f"Reading metadata CSV: {csv_path}")
    summary = detect_hash_duplicates(csv_path, hash_column=hash_column, chunksize=args.chunksize)

    print(f"Total entries: {summary['total']}")
    print(f"Unique {hash_column.upper()}s: {summary['unique']}")
    print(f"Duplicate entries: {summary['duplicates']}")
    print(f"Duplicate percentage: {summary['percentage']:.2f}%")

    # Ensure output directory exists
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        for h in summary["dupe_hashes"]:
            f.write(f"{h}\n")

    print(f"Duplicate {hash_column.upper()}s written to {out_path}")


if __name__ == "__main__":
    main()
