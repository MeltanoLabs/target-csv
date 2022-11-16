"""Tests standard target features using the built-in SDK tests library."""
import shutil
import uuid
from pathlib import Path

import pytest
from singer_sdk.testing import TargetTestRunner, get_test_class, pytest_generate_tests
from singer_sdk.testing.suites import target_tests

from target_csv.target import TargetCSV

test_output_dir = Path(f".output/test_{uuid.uuid4()}/")

SAMPLE_CONFIG = {"max_parallelism": 1, "output_path_prefix": f"{test_output_dir}/"}

StandardTestsTargetCSV = get_test_class(
    test_runner=TargetTestRunner(target_class=TargetCSV, config=SAMPLE_CONFIG),
    test_suites=[target_tests],
)


class TestTargetCSV(StandardTestsTargetCSV):
    @pytest.fixture(scope="class")
    def resource(self):
        test_output_dir.mkdir(parents=True, exist_ok=True)
        yield test_output_dir
        shutil.rmtree(test_output_dir)
