"""CSV target class."""

from singer_sdk import typing as th
from singer_sdk.target_base import Target

from target_csv.sinks import CSVSink


class TargetCSV(Target):
    """A Singer target that generates CSV files."""

    name = "target-csv"
    config_jsonschema = th.PropertiesList(
        th.Property(
            "output_path_prefix",
            th.StringType,
            description=(
                "Optional path prefix which will be prepended to "
                "the file path indicated by `file_naming_schema`."
            ),
        ),
        th.Property(
            "file_naming_scheme",
            th.StringType,
            description=(
                "The scheme with which output files will be named. "
                "Naming scheme may leverage any of the following substitutions: \n\n"
                "- `{stream_name}`"
                "- `{datestamp}`"
                "- `{timestamp}`"
            ),
            default="{stream_name}.csv",
        ),
        th.Property(
            "datestamp_format",
            th.StringType,
            description=(
                "A python format string to use when outputting the `{datestamp}` "
                "string. For reference, see: "
                "https://docs.python.org/3/library/datetime.html"
                "#strftime-and-strptime-format-codes"
            ),
            default="%Y-%m-%d",
        ),
        th.Property(
            "timestamp_format",
            th.StringType,
            description=(
                "A python format string to use when outputting the `{timestamp}` "
                "string. For reference, see: "
                "https://docs.python.org/3/library/datetime.html"
                "#strftime-and-strptime-format-codes"
            ),
            default="%Y-%m-%d.T%H%M%S",
        ),
        th.Property(
            "timestamp_timezone",
            th.StringType,
            description=(
                "The timezone code or name to use when generating "
                "`{timestamp}` and `{datestamp}`. "
                "Defaults to 'UTC'. For a list of possible values, please see: "
                "https://en.wikipedia.org/wiki/List_of_tz_database_time_zones"
            ),
            default="UTC",
        ),
        th.Property(
            "stream_maps",
            th.ObjectType(),
            description=(
                "Allows inline stream transformations and aliasing. "
                "For more information see: "
                "https://sdk.meltano.com/en/latest/stream_maps.html"
            ),
        ),
    ).to_dict()
    default_sink_class = CSVSink
