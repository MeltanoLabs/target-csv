"""CSV target sink class, which handles writing streams."""

import datetime
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import pytz
from singer_sdk import PluginBase
from singer_sdk.sinks import RecordSink

from target_csv.serialization import write_csv, write_csv_header, write_csv_row


class CSVSink(RecordSink):
    """CSV target sink class."""

    max_size = sys.maxsize  # We want all records in one batch
    wrote_header = False

    def __init__(  # noqa: D107
        self,
        target: PluginBase,
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
    def destination_path(self) -> Path:  # noqa: D102
        result = self.config["file_naming_scheme"]
        for key, val in self.filepath_replacement_map.items():
            replacement_pattern = "{" f"{key}" "}"
            if replacement_pattern in result:
                result = result.replace(replacement_pattern, val)

        if self.config.get("output_path_prefix", None) is not None:
            result = f"{self.config['output_path_prefix']}{result}"

        return Path(result)

    def process_record(self, record: dict, context: dict) -> None:
        if not self.wrote_header:
            write_csv_header(self.destination_path, self.schema)
            self.wrote_header = True
        write_csv_row(self.destination_path, record, self.schema)
