"""Tests standard target features using the built-in SDK tests library."""

from typing import Any, Dict

from singer_sdk.testing import get_target_test_class

from target_csv.target import TargetCSV

SAMPLE_CONFIG: Dict[str, Any] = {
    "escape_character": '"',
}

TestTargetCSV = get_target_test_class(TargetCSV, config=SAMPLE_CONFIG)
