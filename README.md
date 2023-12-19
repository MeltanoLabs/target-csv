# `target-csv`

A Singer target that generates CSV files.

Built with the [Meltano SDK](https://sdk.meltano.com) for Singer Taps and Targets.

## Capabilities

* `target`

## Settings

| Setting                  | Required | Default | Description |
|:-------------------------|:--------:|:-------:|:------------|
| output_path              | False    | None    | Filesystem path where to store output files. By default, the current working directory will be used. When specified, the output directory will be created automatically. |
| file_naming_scheme       | False    | {stream_name}.csv    | The scheme with which output files will be named. Naming scheme may leverage any of the following substitutions:<BR/>- `{stream_name}`<BR/>- `{datestamp}`<BR/>- `{timestamp}` |
| datestamp_format         | False    | %Y-%m-%d | A python format string to use when outputting the `{datestamp}` string. For reference, see: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes |
| timestamp_format         | False    | %Y-%m-%d.T%H%M%S | A python format string to use when outputting the `{timestamp}` string. For reference, see: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes |
| timestamp_timezone       | False    | UTC     | The timezone code or name to use when generating `{timestamp}` and `{datestamp}`. Defaults to 'UTC'. For a list of possible values, please see: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones |
| stream_maps              | False    | None    | Allows inline stream transformations and aliasing. For more information see: https://sdk.meltano.com/en/latest/stream_maps.html |
| record_sort_property_name| False    | None    | A property in the record which will be used as a sort key.<BR/><BR/>If this property is omitted, records will not be sorted. |
| overwrite_behavior       | False    | replace_file | Determines the overwrite behavior if destination file already exists. Must be one of the following string values: <BR/><BR/>- `append_records` (default) - append records at the insertion point<BR/>- `replace_file` - replace entire file using `default_CSV_template` |
| escape_characters        | False    | None    | A string of characters to escape when writing CSV files. |

A full list of supported settings and capabilities is available by running: `target-csv --about`

## Installation

```bash
pipx install git+https://github.com/MeltanoLabs/target-csv.git
```

## Usage

You can easily run `target-csv` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Target Directly

```bash
target-csv --version
target-csv --help

# Test using the "Carbon Intensity" sample:
tap-carbon-intensity | target-csv --config /path/to/target-csv-config.json

# Test using the "Smoke Test" tap:
tap-smoke-test --config=tap-smoke-test-config.json | target-csv
```

## Developer Resources

- [ ] `Developer TODO:` As a first step, scan the entire project for the text "`TODO:`" and complete any recommended steps, deleting the "TODO" references once completed.

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `target_csv/tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `target-csv` CLI interface directly using `poetry run`:

```bash
poetry run target-csv --help
```

### Testing with [Meltano](https://meltano.com/)

_**Note:** This target will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Your project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any _"TODO"_ items listed in
the file.

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd target-csv
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke target-csv --version
# OR run a test `elt` pipeline with the Carbon Intensity sample tap:
meltano elt tap-smoke-test target-csv
# Or with debug logging:
meltano --log-level=debug elt tap-smoke-test target-csv
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the Meltano SDK to
develop your own Singer taps and targets.
