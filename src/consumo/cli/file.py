# SPDX-License-Identifier: GPL-3.0-or-later

"""File handler command module."""

import os
from pathlib import Path
from sqlite3 import OperationalError
from typing import Annotated, Callable

import magic
import typer
from pydantic import FilePath, NonNegativeInt, validate_call
from typer import Typer

from consumo.cli.cache import cache_result, get_cached_result
from consumo.cli.config import (
    DEFAULT_CACHE,
    DEFAULT_SKIP_ERRORS,
    DEFAULT_SORT,
    DEFAULT_WORDS_PER_MINUTE,
    CacheOption,
    SkipErrorsOption,
    SortOption,
    WordsPerMinuteOption,
)
from consumo.cli.core import (
    execute_concurrent_command,
)
from consumo.lib.exceptions import UnsupportedMIMETypeError
from consumo.lib.file.html import (
    calculate_consumption_time as calculate_html_consumption_time,
)
from consumo.lib.file.image import calculate_viewing_time
from consumo.lib.file.mass_media import (
    calculate_consumption_time as calculate_mass_media_consumption_time,
)
from consumo.lib.file.multimedia import get_multimedia_duration
from consumo.lib.file.text import (
    calculate_consumption_time as calculate_text_consumption_time,
)

app: Typer = Typer()


@validate_call()
def get_duration(
    file: FilePath, words_per_minute: NonNegativeInt = 265, cache: bool = True
) -> int:
    """Get the duration or calculate the consumption time of a file in seconds.

    Support is based on MIME type.

    Caching is implemented using a SQLite database using mtime for cache
    invalidation.

    Supported types are:

    - "audio": `get_multimedia_duration`.
    - "image": `calculate_viewing_time`.
    - "video": `get_multimedia_duration`.

    Supported types/subtypes are:

    - "application/epub+zip": `calculate_mass_media_consumption_time`.
    - "application/pdf": `calculate_mass_media_consumption_time`.
    - "application/x-mobipocket-ebook": `calculate_mass_media_consumption_time`.
    - "text/html": `calculate_html_consumption_time`.
    - "text/plain": `calculate_text_consumption_time`.

    Directories are unsupported.

    Args:
        file: The path to the file whose duration or consumption time will be
            analyzed.
        words_per_minute: Reading speed in words per minute.
        cache: Whether to cache results in a database for later reuse.
            Values are invalidated based on time.

    Returns:
        The time in seconds to consume the content in the file.

    Raises:
        typer.Exit: Raised with exit code 1 if the MIME type is unsupported.
    """
    absolute_filename: str = str(file.absolute)
    current_time: int | float = os.path.getmtime(file)

    if cache:
        try:
            cached_result: int | None = get_cached_result(
                "consumo", absolute_filename, current_time
            )

            if cached_result is not None:
                return cached_result
        except OperationalError:
            pass

    mime_type: str = magic.from_file(str(file), mime=True)
    type, subtype = mime_type.split("/", 1)
    multimedia_types = ("audio", "video")

    if type == "image":
        return calculate_viewing_time(1)

    if type in multimedia_types:
        return get_multimedia_duration(file)

    mime_type_handler: dict[str, Callable[[Path, NonNegativeInt], int]] = {
        "application/epub+zip": calculate_mass_media_consumption_time,
        "application/pdf": calculate_mass_media_consumption_time,
        "application/x-mobipocket-ebook": calculate_mass_media_consumption_time,
        "text/html": calculate_html_consumption_time,
        "text/plain": calculate_text_consumption_time,
    }

    handler: Callable[[Path, NonNegativeInt], int] | None = mime_type_handler.get(
        mime_type
    )

    if handler is None:
        raise UnsupportedMIMETypeError("File type not supported")

    result: int = handler(file, words_per_minute)

    # Tests can't catch this line for some reason.
    # But they can catch the one from cli/url.py, so we're safe.
    if cache:  # pragma: no cover
        cache_result("consumo", absolute_filename, current_time, result)

    return result


@app.command(
    "file",
    help="Calculate the consumption time of files concurrently in a *h *m *s format.",
)
def process_files(
    files: Annotated[list[Path], typer.Argument(dir_okay=False, exists=True)],
    sort: SortOption = DEFAULT_SORT,
    words_per_minute: WordsPerMinuteOption = DEFAULT_WORDS_PER_MINUTE,
    skip_errors: SkipErrorsOption = DEFAULT_SKIP_ERRORS,
    cache: CacheOption = DEFAULT_CACHE,
) -> None:
    """Calculate the consumption time of files concurrently in a *h *m *s format.

    Args:
        files: The paths to one or multiple files whose consumption time will be
            analyzed.
        sort: Whether to sort output in ascending order.
        words_per_minute: Reading speed in words per minute.
        skip_errors: Whether to warn and return 0 in case an exception is raised
            for a file.
        cache: Whether to cache results in a database for later reuse.
            Values are invalidated based on time.
    """

    def duration_resolver(file: Path) -> int:
        return get_duration(file, words_per_minute, cache)

    execute_concurrent_command(
        files,
        duration_resolver,
        "Processing file(s)...",
        sort=sort,
        skip_errors=skip_errors,
    )
