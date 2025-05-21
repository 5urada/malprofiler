import pandas as pd

def detect_sha256_duplicates(csv_path, chunksize=1_000_000):
    seen = set()
    dupes = set()
    total = 0

    for chunk in pd.read_csv(csv_path, usecols=['sha256'], compression='gzip', chunksize=chunksize):
        for sha in chunk['sha256']:
            total += 1
            if sha in seen:
                dupes.add(sha)
            else:
                seen.add(sha)

    summary = {
        "total": total,
        "unique": len(seen),
        "duplicates": total - len(seen),
        "percentage": (total - len(seen)) / total * 100,
        "dupe_hashes": dupes,
    }
    return summary
