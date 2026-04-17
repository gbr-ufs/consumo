# SPDX-License-Identifier: GPL-3.0-or-later

"""Module for processing files."""

import os
from pathlib import Path
from typing import Any, Callable

import magic
from pydantic import FilePath, NonNegativeInt, validate_call

from consumo.lib.exceptions import NoCacheError, UnsupportedMIMETypeError
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
from consumo.lib.resolvers.core import dummy_cache_resolver, dummy_get_cached_resolver


@validate_call
def get_duration(
    file: FilePath,
    words_per_minute: NonNegativeInt = 265,
    cache: bool = True,
    get_cached_resolver: Callable[[str, str, Any], int] = dummy_get_cached_resolver,
    cache_resolver: Callable[[str, str, int, Any], None] = dummy_cache_resolver,
) -> int:
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
        cache: Whether to cache results in a database for later reuse.
            Values are invalidated based on time.
        get_cached_resolver: Function for getting a value from a cache system
            whose signature consists of program name, key, and time (mtime)
            for cache invalidation.
        cache_resolver: Function for storing a value in a cache system  whose
            signature consists of program name, key, value, and time (mtime) for
            cache invalidation.

    !!! warning

        `get_cached_resolver` and `cache_resolver` have dummy default values. You have
        to implement your own cache functions if you want to use cache!

    Returns:
        The time in seconds to consume the content in the file.

    Raises:
        typer.Exit: Raised with exit code 1 if the MIME type is unsupported.
    """
    absolute_filename: str = str(file.absolute)
    current_time: int | float = os.path.getmtime(file)

    if cache:
        try:
            cached_result: int = get_cached_resolver(
                "consumo", absolute_filename, current_time
            )

            return cached_result
        except NoCacheError:
            pass

    mime_type: str = magic.from_file(str(file), mime=True)
    type, subtype = mime_type.split("/", 1)
    multimedia_types = ("audio", "video")

    if type == "image":
        return calculate_viewing_time(1)

    if type in multimedia_types:
        result: int = get_multimedia_duration(file)

        if cache:
            cache_resolver("consumo", absolute_filename, result, current_time)

        return result

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

    # Covered in `test_get_duration_cache_result`.
    if cache:  # pragma: no cover
        cache_resolver("consumo", absolute_filename, result, current_time)

    return result
