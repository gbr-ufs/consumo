# SPDX-License-Identifier: GPL-3.0-or-later

"""Module for processing multimedia files."""

import math

import av
from pydantic import FilePath, HttpUrl, validate_call

from consumo.lib.exceptions import MissingMetadataError
from consumo.lib.types import DecimalSecond, Second


@validate_call
def get_duration(container: FilePath | HttpUrl) -> Second:
    """Get the duration from a multimedia container or URL.

    Args:
        container: Either a path to a multimedia container or a URL.

    Returns:
        The duration in seconds of the content.

    Raises:
        MissingMetadataError: If the duration can't be found from the metadata.
    """
    av_options: dict[str, str] = {
        # Disables duration analysis, as getting the duration from metadata is
        # faster.
        "analyzeduration": "0",
        # Allocate enough space to probe an integer (32 bits), which will be our
        # duration.
        "probesize": "32",
    }

    with av.open(str(container), options=av_options) as c:
        duration: Second | None = c.duration

        if duration is None:
            raise MissingMetadataError("duration not found")

        # PyAV stores the duration as an integer with more precision than we
        # need (for example, 1 second is equivalent to 1000000).
        # PyAV provides the time_base value to correct this.
        raw_seconds: DecimalSecond = duration / av.time_base

        return math.ceil(raw_seconds)
