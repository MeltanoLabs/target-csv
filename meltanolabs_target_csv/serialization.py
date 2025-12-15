"""Serialization utilities for CSV files."""

from __future__ import annotations

import csv  # noqa: D100
import tempfile
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


def write_csv(
    filepath: Path,
    records: list[dict],
    keys: list[str],
    **kwargs: Any,
) -> int:
    """Write a CSV file."""
    with open(filepath, "w", encoding="utf-8", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=keys, dialect="excel", **kwargs)
        writer.writeheader()
        for record_count, record in enumerate(records, start=1):
            writer.writerow(record)

    return record_count


def write_header(
    filepath: Path, keys: list[str], encoding: str = "utf-8", **kwargs: Any
) -> None:
    """Write a header to a CSV file.

    Creates the parent directory if it doesn't exist.

    Args:
        filepath: Path to the CSV file
        keys: List of column names
        encoding: Character encoding to use (default: utf-8)
        **kwargs: Additional arguments to pass to csv.DictWriter
    """
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with filepath.open("w", encoding=encoding, newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=keys, **kwargs)
        writer.writeheader()


def write_batch(
    filepath: Path,
    records: list[dict],
    keys: list[str],
    encoding: str = "utf-8",
    **kwargs: Any,
) -> None:
    """Write a batch of records to a CSV file.

    Args:
        filepath: Path to the CSV file
        records: List of record dictionaries to write
        keys: List of column names
        encoding: Character encoding to use (default: utf-8)
        **kwargs: Additional arguments to pass to csv.DictWriter
    """
    with tempfile.NamedTemporaryFile("w+", encoding=encoding, newline="") as tmp_fp:
        writer = csv.DictWriter(tmp_fp, fieldnames=keys, **kwargs)
        writer.writerows(records)

        tmp_fp.seek(0)

        with filepath.open("a", encoding=encoding) as f:
            f.write(tmp_fp.read())


def read_csv(filepath: Path) -> list[dict]:
    """Read a CSV file."""
    result: list[dict] = []
    with open(filepath, newline="") as fp:
        reader = csv.DictReader(fp, delimiter=",", dialect="excel")
        result.extend(iter(reader))
    return result
