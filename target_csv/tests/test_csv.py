"""CSV-related tests."""

from typing import Dict, Any, List, Tuple
from pathlib import Path

import pytest

from target_csv.serialization import write_csv, read_csv


SAMPLE_DATASETS: List[Tuple[Dict, List[Dict[str, Any]]]] = [
    (
        # JSON Schema
        {
            "int_key": {"type": "int"},
            "complex_field": {"type": ["object", "null"]},
            "string_field": {"type": "string"},
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


def test_csv_write(output_filepath) -> None:
    for schema, records in SAMPLE_DATASETS:
        write_csv(filepath=output_filepath, records=records, schema=schema)


def test_csv_roundtrip(output_filepath) -> None:
    for schema, records in SAMPLE_DATASETS:
        write_csv(filepath=output_filepath, records=records, schema=schema)
        read_records = read_csv(filepath=output_filepath)
        for orig_record, new_record in zip(records, read_records):
            for key in orig_record.keys():
                # Note: Results are stringified during serialization
                assert str(orig_record[key]) == new_record[key]
