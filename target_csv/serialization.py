import csv  # noqa: D100
from pathlib import Path
from typing import List, Any


def write_csv_header(filepath: Path, schema: dict, **kwargs: Any) -> None:
    """Write a CSV header."""
    if "properties" not in schema:
        raise ValueError("Stream's schema has no properties defined.")

    keys: List[str] = list(schema["properties"].keys())
    with open(filepath, "w", encoding="utf-8", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=keys, dialect="excel", **kwargs)
        writer.writeheader()


def write_csv_row(filepath: Path, record: dict, schema: dict, **kwargs: Any) -> None:
    """Write a CSV row."""
    if "properties" not in schema:
        raise ValueError("Stream's schema has no properties defined.")

    keys: List[str] = list(schema["properties"].keys())
    with open(filepath, "a", encoding="utf-8", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=keys, dialect="excel", **kwargs)
        writer.writerow(record)


def write_csv(filepath: Path, records: List[dict], schema: dict) -> int:
    """Write a CSV file."""
    if "properties" not in schema:
        raise ValueError("Stream's schema has no properties defined.")

    keys: List[str] = list(schema["properties"].keys())
    with open(filepath, "w", encoding="utf-8", newline="") as fp:
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
