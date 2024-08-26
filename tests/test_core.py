"""Tests standard target features using the built-in SDK tests library."""

from pathlib import Path
import sys
from typing import Any, Dict

from singer_sdk.testing import get_target_test_class
from singer_sdk.testing.suites import TestSuite
from singer_sdk.testing.templates import TargetFileTestTemplate

from . import data_files
from target_csv.target import TargetCSV

if sys.version_info >= (3, 9):
    from importlib.resources import files
else:
    from importlib_resources import files

SAMPLE_CONFIG: Dict[str, Any] = {
    "escape_character": "\\",
}


class MultipleStreamsTest(TargetFileTestTemplate):
    name = "users_and_employees"

    @property
    def singer_filepath(self) -> Path:
        return files(data_files) / f"{self.name}.singer"


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
