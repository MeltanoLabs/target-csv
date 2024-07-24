"""CSV-related tests."""

from pathlib import Path
from typing import Any, Dict, List, Tuple

import pytest

from target_csv.serialization import read_csv, write_csv

SAMPLE_DATASETS: List[Tuple[Dict, List[Dict[str, Any]]]] = [
    (
        # JSON Schema
        {
            "properties": {
                "int_key": {"type": "int"},
                "complex_field": {"type": ["object", "null"]},
                "string_field": {"type": "string"},
            }
        },
        # Records
        [
            {"int_key": 1, "string_field": "hello", "complex_field": {}},
            {"int_key": 2, "complex_field": {"foo": "bar"}, "string_field": "hello"},
            # Fields out of order:
            {
                "int_key": 3,
                "string_field": "hello",
                "complex_field": {"foo": "bar"},
            },
            # Special characters in string:
            {"int_key": 4, "string_field": "''he\\l|,o\"\\n", "complex_field": {}},
            # Newline characters in string:
            {
                "int_key": 5,
                "complex_field": {},
                "string_field": "hello\nworld",
            },
        ],
    )
]


@pytest.fixture
def output_dir() -> Path:
    result = Path("./.output/")
    if not result.is_dir():
        result.mkdir()

    return result


@pytest.fixture
def output_filepath(output_dir) -> Path:
    result = Path(output_dir / "csv-test-output.csv")
    if result.exists():
        result.unlink()

    return result


@pytest.fixture
def test_file_paths(output_dir) -> List[Path]:
    paths = []
    for dir in range(4):
        path = Path(output_dir / f"test-dir-{dir}/csv-test-output-{dir}.csv")
        path.unlink(missing_ok=True)
        paths.append(path)
    return paths


def test_csv_write(output_filepath) -> None:
    for schema, records in SAMPLE_DATASETS:
        write_csv(filepath=output_filepath, records=records, schema=schema)


def test_csv_write_if_not_exists(test_file_paths) -> None:
    for path in test_file_paths:
        for schema, records in SAMPLE_DATASETS:
            write_csv(filepath=path, records=records, schema=schema)


def test_csv_roundtrip(output_filepath) -> None:
    for schema, records in SAMPLE_DATASETS:
        write_csv(filepath=output_filepath, records=records, schema=schema)
        read_records = read_csv(filepath=output_filepath)
        for orig_record, new_record in zip(records, read_records):
            for key in orig_record.keys():
                # Note: Results are stringified during serialization
                assert str(orig_record[key]) == new_record[key]
