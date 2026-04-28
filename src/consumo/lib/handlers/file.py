# SPDX-FileCopyrightText: 2026 Gabriel Santos de Souza <gabriel.santosdesouza@dcomp.ufs.br>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Module for processing files."""

from pathlib import Path
from typing import Callable

import magic
from pydantic import FilePath, NonNegativeInt, validate_call

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


@validate_call
def get_duration(
    file: FilePath,
    words_per_minute: NonNegativeInt = 265,
) -> int:
    """Get the duration or calculate the consumption time of a file in seconds.

    Support is based on MIME type.

    Supported types are:

    - "audio": [`get_multimedia_duration`][consumo.get_multimedia_duration].
    - "image": [`calculate_viewing_time`][consumo.calculate_viewing_time].
    - "video": [`get_multimedia_duration`][consumo.get_multimedia_duration].

    Supported types/subtypes are:

    - "application/epub+zip": [`calculate_mass_media_consumption_time`][consumo.calculate_mass_media_consumption_time].
    - "application/pdf": [`calculate_mass_media_consumption_time`][consumo.calculate_mass_media_consumption_time].
    - "application/x-mobipocket-ebook": [`calculate_mass_media_consumption_time`][consumo.calculate_mass_media_consumption_time].
    - "text/html": [`calculate_html_consumption_time`][consumo.calculate_html_consumption_time].
    - "text/plain": [`calculate_text_consumption_time`][consumo.calculate_text_consumption_time].

    Directories are unsupported.

    Args:
        file: The path to the file whose duration or consumption time will be
            analyzed.
        words_per_minute: Reading speed in words per minute.

    Returns:
        The time in seconds to consume the content in the file.

    Raises:
        UnsupportedMIMETypeError: When the MIME type is unsupported.
    """
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

    return handler(file, words_per_minute)
