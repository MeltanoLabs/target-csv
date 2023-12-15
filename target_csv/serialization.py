import csv  # noqa: D100
from pathlib import Path
from typing import Any, List


def write_csv(filepath: Path, records: List[dict], schema: dict, **kwargs: Any) -> int:
    """Write a CSV file."""
    if "properties" not in schema:
        raise ValueError("Stream's schema has no properties defined.")

    keys: List[str] = list(schema["properties"].keys())
    with open(filepath, "w", encoding="utf-8", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=keys, dialect="excel", **kwargs)
        writer.writeheader()
        for record_count, record in enumerate(records, start=1):
            writer.writerow(record)

    return record_count


def read_csv(filepath: Path) -> List[dict]:
    """Read a CSV file."""
    result: List[dict] = []
    with open(filepath, newline="") as fp:
        reader = csv.DictReader(fp, delimiter=",", dialect="excel")
        result.extend(iter(reader))
    return result
