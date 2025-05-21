import pandas as pd

def detect_hash_duplicates(csv_path, hash_column='sha256', chunksize=1_000_000):
    """
    Detect duplicates in the specified hash column of a gzip-compressed CSV.
    
    Args:
        csv_path (str or Path): Path to the .csv.gz metadata file.
        hash_column (str): Name of the column to dedupe on ('sha256', 'md5', etc.).
        chunksize (int): Number of rows per pandas chunk.
    
    Returns:
        dict: {
            'total': total rows processed,
            'unique': number of unique hashes,
            'duplicates': number of duplicate entries,
            'percentage': percentage of duplicates,
            'dupe_hashes': set of duplicated hash values
        }
    """
    seen = set()
    dupes = set()
    total = 0

    for chunk in pd.read_csv(
        csv_path,
        usecols=[hash_column],
        compression='gzip',
        chunksize=chunksize
    ):
        for h in chunk[hash_column]:
            total += 1
            if h in seen:
                dupes.add(h)
            else:
                seen.add(h)

    return {
        "total": total,
        "unique": len(seen),
        "duplicates": total - len(seen),
        "percentage": (total - len(seen)) / total * 100,
        "dupe_hashes": dupes,
    }
