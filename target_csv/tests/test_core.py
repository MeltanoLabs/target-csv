"""Tests standard target features using the built-in SDK tests library."""

from singer_sdk.testing import TargetTestRunner, get_test_class
from singer_sdk.testing.suites import target_tests

from target_csv.target import TargetCSV

SAMPLE_CONFIG = {
    "max_parallelism": 1,
}

TestTargetCSV = get_test_class(
    test_runner_class=TargetTestRunner,
    test_runner_kwargs=dict(target_class=TargetCSV, config=SAMPLE_CONFIG),
    test_suites=[target_tests],
)
