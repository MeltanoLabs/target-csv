"""Tests standard target features using the built-in SDK tests library."""

from pathlib import Path
from typing import Any, Dict

from singer_sdk.testing import get_target_test_class
from singer_sdk.testing.suites import TestSuite
from singer_sdk.testing.templates import TargetFileTestTemplate

from target_csv.target import TargetCSV

SAMPLE_CONFIG: Dict[str, Any] = {
    "escape_character": '"',
}


class MultipleStreamsTest(TargetFileTestTemplate):
    name = "users_and_employees"

    @property
    def singer_filepath(self) -> Path:
        current_dir = Path(__file__).resolve().parent
        return current_dir / "data_files" / f"{self.name}.singer"


TestTargetCSV = get_target_test_class(
    TargetCSV,
    config=SAMPLE_CONFIG,
    custom_suites=[
        TestSuite(
            kind="target",
            tests=[MultipleStreamsTest],
        )
    ],
)
