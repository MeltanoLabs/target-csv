"""CSV-related tests."""

import io
from pathlib import Path
from typing import Any, Dict, List, Tuple
from contextlib import redirect_stdout
import shutil

import pytest

from target_csv.serialization import read_csv, write_csv
from target_csv.target import TargetCSV

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

def singer_file_to_target(file_name, target) -> None:
    """Singer file to Target, emulates a tap run

    Equivalent to running cat file_path | target-name --config config.json.
    Note that this function loads all lines into memory, so it is
    not good very large files.

    Args:
        file_name: name to file in .tests/data_files to be sent into target
        Target: Target to pass data from file_path into..
    """
    file_path = Path(__file__).parent / Path("./data_files") / Path(file_name)
    buf = io.StringIO()
    with redirect_stdout(buf):
        with open(file_path) as f:
            for line in f:
                print(line.rstrip("\r\n"))  # File endings are here,
                # and print adds another line ending so we need to remove one.
    buf.seek(0)
    target.listen(buf)

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

def test_csv_multiple_streams(output_dir) -> None:
    """Tests syncing multiple streams. 30 times in a row to catch race condition.
    
    Further discussion in #129.
    """
    file_name = "users_and_employees.singer"
    for i in range(30):
        path = Path(output_dir / "test_csv_multiple_streams" / f"{i}")
        shutil.rmtree(path, ignore_errors=True)
        singer_file_to_target(
            file_name=file_name,
            target=TargetCSV(config={"output_path": str(path)})
        )