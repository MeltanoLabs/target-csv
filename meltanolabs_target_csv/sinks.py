"""CSV target sink class, which handles writing streams."""

from __future__ import annotations

import datetime
import functools
import sys
import warnings
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pytz
from singer_sdk.sinks import BatchSink

from meltanolabs_target_csv.serialization import write_batch, write_header

if TYPE_CHECKING:
    from singer_sdk import Target


class CSVSink(BatchSink):
    """CSV target sink class."""

    MAX_SIZE_DEFAULT = sys.maxsize

    def __init__(  # noqa: D107
        self,
        target: Target,
        stream_name: str,
        schema: dict,
        key_properties: list[str] | None,
    ) -> None:
        self._timestamp_time: datetime.datetime | None = None
        super().__init__(target, stream_name, schema, key_properties)

    @property
    def timestamp_time(self) -> datetime.datetime:  # noqa: D102
        if not self._timestamp_time:
            self._timestamp_time = datetime.datetime.now(
                tz=pytz.timezone(self.config["timestamp_timezone"])
            )

        return self._timestamp_time

    @property
    def filepath_replacement_map(self) -> dict[str, str]:  # noqa: D102
        return {
            "stream_name": self.stream_name,
            "datestamp": self.timestamp_time.strftime(self.config["datestamp_format"]),
            "timestamp": self.timestamp_time.strftime(self.config["timestamp_format"]),
        }

    @property
    def output_file(self) -> Path:  # noqa: D102
        filename = self.config["file_naming_scheme"]
        for key, val in self.filepath_replacement_map.items():
            replacement_pattern = f"{{{key}}}"
            if replacement_pattern in filename:
                filename = filename.replace(replacement_pattern, val)

        if "output_path_prefix" in self.config:
            warnings.warn(
                "The property `output_path_prefix` is deprecated, "
                "please use `output_path`.",
                category=UserWarning,
            )

        # Accept all possible properties defining the output path.
        # - output_path: The new designated property.
        # - destination_path: Alias for `output_path` (`hotgluexyz` compat).
        # - output_path_prefix: The property used up until now.
        output_path = self.config.get(
            "output_path",
            self.config.get(
                "destination_path", self.config.get("output_path_prefix", None)
            ),
        )

        filepath = Path(filename)
        if output_path is not None:
            filepath = Path(output_path) / filepath

        return filepath

    @functools.cached_property
    def keys(self) -> list[str]:
        """Get the header keys for the CSV file."""
        if "properties" not in self.schema:
            raise ValueError("Stream's schema has no properties defined")

        return list(self.schema["properties"].keys())

    @functools.cached_property
    def escape_character(self) -> str | None:
        """Get the escape character for the CSV file."""
        return self.config.get("escape_character")

    def setup(self) -> None:
        """Create the output file and write the header."""
        super().setup()
        output_file = self.output_file
        self.logger.info("Writing to destination file '%s'...", output_file.resolve())
        write_header(
            output_file,
            self.keys,
            dialect="excel",
            escapechar=self.escape_character,
        )

    def process_batch(self, context: dict) -> None:
        """Write out any prepped records and return once fully written."""
        output_file: Path = self.output_file

        if not isinstance(context["records"], list):
            self.logger.warning("No values in %s records collection.", self.stream_name)
            context["records"] = []

        records: list[dict[str, Any]] = context["records"]
        if "record_sort_property_name" in self.config:
            sort_property_name = self.config["record_sort_property_name"]
            records = sorted(records, key=lambda x: x[sort_property_name])

        self.logger.info(f"Appending {len(records)} records to file...")

        write_batch(
            output_file,
            records,
            self.keys,
            dialect="excel",
            escapechar=self.escape_character,
        )
