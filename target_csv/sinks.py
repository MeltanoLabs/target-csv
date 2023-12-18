"""CSV target sink class, which handles writing streams."""

import datetime
import sys
import warnings
from pathlib import Path
from typing import Any, Dict, List, Optional

import pytz
from singer_sdk import Target
from singer_sdk.sinks import BatchSink

from target_csv.serialization import write_csv


class CSVSink(BatchSink):
    """CSV target sink class."""

    max_size = sys.maxsize  # We want all records in one batch

    def __init__(  # noqa: D107
        self,
        target: Target,
        stream_name: str,
        schema: Dict,
        key_properties: Optional[List[str]],
    ) -> None:
        self._timestamp_time: Optional[datetime.datetime] = None
        super().__init__(target, stream_name, schema, key_properties)

    @property
    def timestamp_time(self) -> datetime.datetime:  # noqa: D102
        if not self._timestamp_time:
            self._timestamp_time = datetime.datetime.now(
                tz=pytz.timezone(self.config["timestamp_timezone"])
            )

        return self._timestamp_time

    @property
    def filepath_replacement_map(self) -> Dict[str, str]:  # noqa: D102
        return {
            "stream_name": self.stream_name,
            "datestamp": self.timestamp_time.strftime(self.config["datestamp_format"]),
            "timestamp": self.timestamp_time.strftime(self.config["timestamp_format"]),
        }

    @property
    def output_file(self) -> Path:  # noqa: D102
        filename = self.config["file_naming_scheme"]
        for key, val in self.filepath_replacement_map.items():
            replacement_pattern = "{" f"{key}" "}"
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

    def process_batch(self, context: dict) -> None:
        """Write out any prepped records and return once fully written."""
        output_file: Path = self.output_file
        self.logger.info(f"Writing to destination file '{output_file.resolve()}'...")
        new_contents: dict  # noqa: F842
        create_new = (
            self.config["overwrite_behavior"] == "replace_file"
            or not output_file.exists()
        )
        if not create_new:
            raise NotImplementedError("Append mode is not yet supported.")

        if not isinstance(context["records"], list):
            self.logger.warning(f"No values in {self.stream_name} records collection.")
            context["records"] = []

        records: List[Dict[str, Any]] = context["records"]
        if "record_sort_property_name" in self.config:
            sort_property_name = self.config["record_sort_property_name"]
            records = sorted(records, key=lambda x: x[sort_property_name])

        self.logger.info(f"Writing {len(context['records'])} records to file...")

        write_csv(
            output_file,
            context["records"],
            self.schema,
            escapechar=self.config.get("escape_character"),
        )
