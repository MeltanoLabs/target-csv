import csv
from typing import Any, Dict, Iterable, List
from pathlib import Path


def write_csv(filepath: Path, records: List[dict], schema: dict) -> int:
    """Write a CSV file."""
    keys: List[str] = list(schema.keys())
    with open(filepath, "wt", encoding="utf-8", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=keys, dialect="excel")
        writer.writeheader()
        for record_count, record in enumerate(records, start=1):
            writer.writerow(record)

    return record_count


def read_csv(filepath: Path) -> List[dict]:
    """Read a CSV file."""
    result: List[dict] = []
    with open(filepath, newline="") as fp:
        reader = csv.DictReader(fp, delimiter=",", dialect="excel")
        for record in reader:
            result.append(record)

    return result
