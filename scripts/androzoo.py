import sys
from pathlib import Path
import argparse

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from utils.dedup_utils import detect_hash_duplicates


def main():
    parser = argparse.ArgumentParser(
        description="Detect hash duplicates in AndroZoo metadata CSV for SHA256, SHA1, and MD5"
    )
    parser.add_argument(
        "-i", "--input",
        type=Path,
        default=project_root / "datasets" / "latest_with-added-date.csv.gz",
        help="Path to the gzipped metadata CSV file"
    )
    parser.add_argument(
        "-o", "--output-dir",
        type=Path,
        default=project_root / "results",
        help="Directory to write duplicate hash values"
    )
    parser.add_argument(
        "-c", "--chunksize",
        type=int,
        default=1_000_000,
        help="Number of rows per pandas chunk"
    )
    args = parser.parse_args()

    csv_path = args.input
    output_dir = args.output_dir
    chunksize = args.chunksize

    print(f"Reading metadata CSV: {csv_path}")
    hash_columns = ["sha256", "sha1", "md5"]
    for hash_column in hash_columns:
        print(f"\nProcessing duplicates for {hash_column.upper()}...")
        summary = detect_hash_duplicates(csv_path, hash_column=hash_column, chunksize=chunksize)

        print(f"Total entries: {summary['total']}")
        print(f"Unique {hash_column.upper()}s: {summary['unique']}")
        print(f"Duplicate entries: {summary['duplicates']}")
        print(f"Duplicate percentage: {summary['percentage']:.2f}%")

        # Ensure output directory exists
        output_dir.mkdir(parents=True, exist_ok=True)
        out_file = output_dir / f"duplicate_{hash_column}.txt"
        with open(out_file, "w") as f:
            for h in summary["dupe_hashes"]:
                f.write(f"{h}\n")
        print(f"Duplicate {hash_column.upper()}s written to {out_file}")

if __name__ == "__main__":
    main()
