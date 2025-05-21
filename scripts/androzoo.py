from pathlib import Path
from utils.dedup_utils import detect_sha256_duplicates

csv_path = Path("../datasets/latest_with-added-date.csv.gz")
out_path = Path("../results/_androzoo_duplicate_sha256s.txt")

summary = detect_sha256_duplicates(csv_path)

print(f"Total entries: {summary['total']}")
print(f"Unique SHA256s: {summary['unique']}")
print(f"Duplicate entries: {summary['duplicates']}")
print(f"Duplicate percentage: {summary['percentage']:.2f}%")

# Save hashes
with open(out_path, "w") as f:
    for sha in summary["dupe_hashes"]:
        f.write(f"{sha}\n")
