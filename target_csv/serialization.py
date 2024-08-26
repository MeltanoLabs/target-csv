import csv  # noqa: D100
import sys
from pathlib import Path
from typing import Any, List, Callable, TypeVar

if sys.version_info < (3, 10):
    from typing_extensions import Concatenate, ParamSpec
else:
    from typing import Concatenate, ParamSpec

P = ParamSpec("P")
T = TypeVar("T")


def create_folder_if_not_exists(
    func: Callable[Concatenate[Path, P], T],
) -> Callable[Concatenate[Path, P], T]:
    """Decorator to create folder if it does not exist."""

    def wrapper(filepath: Path, *args: P.args, **kwargs: P.kwargs) -> T:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        return func(filepath, *args, **kwargs)

    return wrapper


@create_folder_if_not_exists
def write_csv(filepath: Path, records: List[dict], schema: dict, **kwargs: Any) -> int:
    """Write a CSV file."""
    if "properties" not in schema:
        raise ValueError("Stream's schema has no properties defined.")

    keys: List[str] = list(schema["properties"].keys())
    with open(filepath, "w", encoding="utf-8", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=keys, dialect="excel", **kwargs)
        writer.writeheader()
        for record_count, record in enumerate(records, start=1):
            writer.writerow(record)

    return record_count


def read_csv(filepath: Path) -> List[dict]:
    """Read a CSV file."""
    result: List[dict] = []
    with open(filepath, newline="") as fp:
        reader = csv.DictReader(fp, delimiter=",", dialect="excel")
        result.extend(iter(reader))
    return result
