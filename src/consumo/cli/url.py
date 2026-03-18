# SPDX-License-Identifier: GPL-3.0-or-later

"""URL handler command module."""

from typing import Annotated

import typer
from av.error import FFmpegError
from pydantic import (
    HttpUrl,
    NonNegativeInt,
    validate_call,
)
from typer import Typer
from yt_dlp.utils import DownloadError

from consumo.cli.config import (
    DEFAULT_SORT,
    DEFAULT_WORDS_PER_MINUTE,
    SortOption,
    WordsPerMinuteOption,
)
from consumo.cli.core import (
    execute_concurrent_command,
)
from consumo.lib.exceptions import MissingMetadataError
from consumo.lib.file.multimedia import (
    get_hosted_multimedia_duration,
    get_multimedia_duration,
)
from consumo.lib.url import calculate_consumption_time

app: Typer = Typer()


@validate_call
def get_duration(url: HttpUrl, words_per_minute: NonNegativeInt = 265) -> int:
    """Get the duration or calculate the consumption time of a URL in seconds.

    Gets the duration of media from hosting platforms or direct file
    links, and calculates the consumption time otherwise.

    Args:
        url: The URL of the content whose duration or consumption time will be
            analyzed.
        words_per_minute: Reading speed in words per minute.

    Returns:
        The time in seconds to consume the content the URL points to.
    """
    # Fallback mechanism. First we try to get the duration as if its was hosted
    # on a platform, then as a hosted file, and when all else fails, we try to
    # calculate the consumption time.
    try:
        return get_hosted_multimedia_duration(url)
    except DownloadError:
        pass
    except MissingMetadataError:
        pass

    try:
        return get_multimedia_duration(url)
    except FFmpegError:
        pass

    return calculate_consumption_time(url, words_per_minute)


@app.command(
    "url",
    help="Calculate the consumption time of URLs concurrently in a *h *m *s format.",
)
def process_urls(
    urls: Annotated[list[str], typer.Argument()],
    sort: SortOption = DEFAULT_SORT,
    words_per_minute: WordsPerMinuteOption = DEFAULT_WORDS_PER_MINUTE,
) -> None:
    """Calculate the consumption time of URLs concurrently in a *h *m *s format.

    Args:
        urls: A list of URLs pointing to the content whose consumption time
            will be analyzed.
        sort: Whether to sort output in ascending order.
        words_per_minute: Reading speed in words per minute.
    """

    def duration_resolver(url: str) -> int:
        return get_duration(HttpUrl(url), words_per_minute)

    execute_concurrent_command(
        urls, duration_resolver, "Processing URL(s)...", sort=sort
    )
