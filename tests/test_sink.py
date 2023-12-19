from pathlib import Path

import pytest

from target_csv.sinks import CSVSink
from target_csv.target import TargetCSV


def test_sink_output_file_cwd():
    """Verify `output_file` property without defining an output path."""
    target = TargetCSV()
    sink = CSVSink(
        target=target, stream_name="foo", schema={"properties": {}}, key_properties=[]
    )
    assert sink.output_file == Path("foo.csv")


@pytest.mark.parametrize(
    "property_name", ["output_path", "destination_path", "output_path_prefix"]
)
def test_sink_output_file_with_path(tmp_path, property_name):
    """Verify `output_file` property when defining an output path.

    The test is parameterized to iterate and verify all the possible properties
    which define an output path.
    """
    folder_path = tmp_path / "to/folder"
    output_file = tmp_path / "to/folder/foo.csv"
    target = TargetCSV(config={property_name: str(folder_path)})
    sink = CSVSink(
        target=target, stream_name="foo", schema={"properties": {}}, key_properties=[]
    )
    assert sink.output_file == output_file


def test_sink_output_file_with_path_deprecated(tmp_path):
    """Verify `output_file` property with deprecated `output_path_prefix` property."""
    folder_path = tmp_path / "to/folder"
    output_file = tmp_path / "to/folder/foo.csv"
    target = TargetCSV(config={"output_path_prefix": str(folder_path)})
    sink = CSVSink(
        target=target, stream_name="foo", schema={"properties": {}}, key_properties=[]
    )
    with pytest.warns(
        UserWarning,
        match="The property `output_path_prefix` is deprecated, "
        "please use `output_path`.",
    ):
        assert sink.output_file == output_file
