# SPDX-License-Identifier: GPL-3.0-or-later

"""Module for processing multimedia files."""

import math
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Iterator

import av
from pydantic import FilePath, HttpUrl, validate_call
from yt_dlp import DownloadError, YoutubeDL

from consumo.lib.classes import SilentLogger
from consumo.lib.exceptions import MissingMetadataError


def duration_resolver(entry: dict[str, Any]) -> int:
    """Get the duration of multimedia from a dictionary.

    Args:
        entry: Dictionary potentially containing a duration entry.

    Returns:
        The duration of the content in seconds.
    """
    raw_duration: float | None = entry.get("duration")

    if raw_duration is None:
        raise MissingMetadataError("duration not found")

    return math.ceil(raw_duration)


@validate_call
def get_hosted_multimedia_duration(url: HttpUrl) -> int:
    """Get the duration of a multimedia container from a hosting platform.

    Supports playlists.

    Args:
        url: The URL pointing to where the multimedia container is hosted.

    Returns:
        The duration in seconds of the content.

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

        # This means that the link points to a playlist.
        if info.get("entries"):
            entries: list[dict[str, Any]] = info["entries"]
            total_duration: int = 0

            with ThreadPoolExecutor() as e:
                resolved_durations: Iterator[int] = e.map(duration_resolver, entries)

                total_duration += sum(resolved_durations)

                return total_duration

        return duration_resolver(info)


@validate_call
def get_multimedia_duration(container: FilePath | HttpUrl) -> int:
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
        duration: int | None = c.duration

        if duration is None:
            raise MissingMetadataError("duration not found")

        # PyAV stores the duration as an integer with more precision than we
        # need (for example, 1 second is equivalent to 1000000).
        # PyAV provides the time_base value to correct this.
        raw_seconds: float = duration / av.time_base

        return math.ceil(raw_seconds)


def get_duration(url: HttpUrl) -> int:
    """Get the duration of a multimedia container hosted online.

    Tries to treat the URL as if it was from a hosting platform, then tries to
    get the duration from the container as if the URL pointed directly to it if
    that fails.

    Args:
        url: URL pointing to where the multimedia container is hosted.

    Returns:
        The duration of the content in seconds.
    """
    try:
        duration: int = get_hosted_multimedia_duration(url)
    except (DownloadError, MissingMetadataError):
        duration: int = get_multimedia_duration(url)

    return duration
