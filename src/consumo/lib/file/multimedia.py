# SPDX-License-Identifier: GPL-3.0-or-later

import math

import av
from pydantic import FilePath, HttpUrl, validate_call

from consumo.lib.exceptions import MissingMetadataError
from consumo.lib.types import DecimalSecond, Second


@validate_call
def get_duration(container: FilePath | HttpUrl) -> Second:
    av_options: dict[str, str] = {"analyzeduration": "0", "probesize": "32"}

    with av.open(str(container), options=av_options) as c:
        duration: Second | None = c.duration

        if duration is None:
            raise MissingMetadataError("duration not found")

        raw_seconds: DecimalSecond = duration / av.time_base

        return math.ceil(raw_seconds)
