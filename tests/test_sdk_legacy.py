"""Tests standard target features using the built-in SDK tests library."""

from typing import Any, Dict

from singer_sdk.testing import get_standard_target_tests

from target_csv.target import TargetCSV

SAMPLE_CONFIG: Dict[str, Any] = {
    # TODO: Initialize minimal target config
}


# Run standard built-in target tests from the SDK:
def test_standard_target_tests():
    """Run standard target tests from the SDK."""
    tests = get_standard_target_tests(
        TargetCSV,
        config=SAMPLE_CONFIG,
    )
    for test in tests:
        test()


# TODO: Create additional tests as appropriate for your target.
