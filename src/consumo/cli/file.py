# SPDX-License-Identifier: GPL-3.0-or-later

"""File handler command module."""

from pathlib import Path
from typing import Annotated, Callable

import magic
import typer
from pydantic import PositiveInt, validate_call
from typer import Typer

from consumo.cli.core import (
    SortOption,
    WordsPerMinuteOption,
    execute_concurrent_command,
    unsupported_mime_type_error,
)
from consumo.lib.file.html import (
    calculate_consumption_time as calculate_html_consumption_time,
)
from consumo.lib.file.image import calculate_viewing_time
from consumo.lib.file.mass_media import (
    calculate_consumption_time as calculate_mass_media_consumption_time,
)
from consumo.lib.file.multimedia import get_duration as get_multimedia_duration
from consumo.lib.file.text import (
    calculate_consumption_time as calculate_text_consumption_time,
)
from consumo.lib.types import Second

app: Typer = Typer()


@validate_call()
def get_duration(file: Path, words_per_minute: PositiveInt = 265) -> Second:
    """Get the duration or calculate the consumption time of a file in seconds.

    Support is based on MIME type.

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

    Returns:
        The time in seconds to consume the content in the file.

    Raises:
        IsADirectoryError: If the file path points to a directory.
        typer.Exit: Raised with exit code 1 if the MIME type is unsupported.
    """
    if file.is_dir():
        raise IsADirectoryError

    # Cast to str because python-magic-bin is behind python-magic in version
    # and thus doesn't support the Path type.
    mime_type: str = magic.from_file(str(file), mime=True)
    type, subtype = mime_type.split("/", 1)
    multimedia_types = ("audio", "video")

    if type == "image":
        return calculate_viewing_time(1)

    if type in multimedia_types:
        return get_multimedia_duration(file)

    mime_type_handler: dict[str, Callable[[Path, PositiveInt], Second]] = {
        "application/epub+zip": calculate_mass_media_consumption_time,
        "application/pdf": calculate_mass_media_consumption_time,
        "application/x-mobipocket-ebook": calculate_mass_media_consumption_time,
        "text/html": calculate_html_consumption_time,
        "text/plain": calculate_text_consumption_time,
    }

    handler: Callable[[Path, PositiveInt], Second] | None = mime_type_handler.get(
        mime_type
    )

    if handler is None:
        unsupported_mime_type_error(mime_type)

        raise typer.Exit(1)

    return handler(file, words_per_minute)


@app.command("file")
def process_files(
    files: Annotated[list[Path], typer.Argument(exists=True, readable=True)],
    sort: SortOption = False,
    words_per_minute: WordsPerMinuteOption = 265,
) -> None:
    """Calculate the consumption time of files concurrently in a *h *m *s format.

    Args:
        files: The paths to one or multiple files whose consumption time will be
            analyzed.
        sort: Whether to sort output in ascending order.
        words_per_minute: Reading speed in words per minute.
    """

    def duration_resolver(file: Path) -> Second:
        return get_duration(file, words_per_minute)

    execute_concurrent_command(
        files, duration_resolver, "Processing file(s)...", sort=sort
    )
