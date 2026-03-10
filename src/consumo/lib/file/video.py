# SPDX-License-Identifier: GPL-3.0-or-later

"""Module for processing online videos."""

import math
from typing import Any

from pydantic import HttpUrl, validate_call
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

from consumo.lib.classes import SilentLogger
from consumo.lib.exceptions import MissingMetadataError
from consumo.lib.file.multimedia import get_duration as get_multimedia_duration
from consumo.lib.types import DecimalSecond, Second


@validate_call
def get_video_platform_video_duration(url: HttpUrl) -> Second:
    """Get the duration of a video hosted on a platform.

    Args:
        url: The URL pointing to where the video is hosted.

    Returns:
        The duration of the video in seconds.

    Raises:
        MissingMetadataError: If the duration can't be found from the metadata.
    """
    ytdl_options: dict[str, Any] = {
        # Silenced to prevent messages from leaking into the program.
        "logger": SilentLogger(),
        "no_warnings": True,
        "quiet": True,
    }

    with YoutubeDL(ytdl_options) as ytdl:
        # Downloads are disabled so we only fetch metadata.
        info: dict[str, Any] = ytdl.extract_info(str(url), download=False)
        raw_duration: DecimalSecond = info.get("duration")

        if raw_duration is None:
            raise MissingMetadataError("duration not found")

        duration: Second = math.ceil(raw_duration)

        return duration


def get_duration(url: HttpUrl) -> Second:
    """Get the duration of a video hosted online.

    Tries to treat the URL as if it was from a video hosting platform, then tries
    to get the duration from the video as if the URL pointed directly to a file
    if that fails.

    Args:
        url: URL pointing to where the video is hosted.

    Returns:
        The duration of the video in seconds.
    """
    try:
        duration: Second = get_video_platform_video_duration(url)
    except (DownloadError, MissingMetadataError):
        duration: Second = get_multimedia_duration(url)

    return duration
