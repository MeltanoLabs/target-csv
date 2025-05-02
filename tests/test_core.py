"""Tests standard target features using the built-in SDK tests library."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from singer_sdk.testing import get_target_test_class
from singer_sdk.testing.suites import TestSuite
from singer_sdk.testing.templates import TargetFileTestTemplate

from target_csv.target import TargetCSV

from . import data_files

from importlib.resources import files

if TYPE_CHECKING:
    from importlib.abc import Traversable

SAMPLE_CONFIG: dict[str, Any] = {
    "escape_character": "\\",
}


class MultipleStreamsTest(TargetFileTestTemplate):
    name = "users_and_employees"

    @property
    def singer_filepath(self) -> Traversable:
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
