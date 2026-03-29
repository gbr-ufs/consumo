# SPDX-License-Identifier: GPL-3.0-or-later

"""URL handler command module."""

import urllib.request
from datetime import date
from sqlite3 import OperationalError
from typing import Annotated
from urllib.parse import urljoin

import courlan
import typer
from av.error import FFmpegError
from bs4 import BeautifulSoup, ResultSet, Tag
from bs4.element import AttributeValueList
from pydantic import (
    HttpUrl,
    NonNegativeInt,
    validate_call,
)
from typer import Typer
from yt_dlp.utils import DownloadError

from consumo.cli.cache import cache_result, get_cached_result
from consumo.cli.config import (
    DEFAULT_DEPTH,
    DEFAULT_SKIP_ERRORS,
    DEFAULT_SORT,
    DEFAULT_WORDS_PER_MINUTE,
    DepthOption,
    SkipErrorsOption,
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
def get_duration(
    url: HttpUrl,
    words_per_minute: NonNegativeInt = 265,
    depth: NonNegativeInt = 0,
) -> int:
    """Get the duration or calculate the consumption time of a URL in seconds.

    Gets the duration of media from hosting platforms or direct file
    links, and calculates the consumption time otherwise.

    Caching is implemented using a SQLite database. A cache is valid for one
    day.

    Args:
        url: The URL of the content whose duration or consumption time will be
            analyzed.
        words_per_minute: Reading speed in words per minute.

    Returns:
        The time in seconds to consume the content the URL points to.
    """
    # not_iterable is ignored for this line because courlan.check_url only
    # returns None if there is no domain. This is unlikely to happen, as
    # Pydantic would catch that before the url even reaches this part of the
    # function.
    normalized_url, _ = courlan.check_url(str(url))  # ty:ignore[not-iterable]
    key: str = f"{normalized_url}:{words_per_minute}:{depth}"
    current_time: str = date.today().isoformat()

    try:
        cached: int | None = get_cached_result("consumo", key, current_time)

        if cached is not None:
            return cached
    except OperationalError:
        pass

    # Fallback mechanism. First we try to get the duration as if it was hosted
    # on a platform, then as a hosted file, and when all else fails, we try to
    # calculate the consumption time.
    result: int | None = None

    try:
        result: int = get_hosted_multimedia_duration(url)
    except (DownloadError, MissingMetadataError):
        pass

    if result is None:
        try:
            result: int = get_multimedia_duration(url)
        except FFmpegError:
            pass

    if result is None:
        result: int = calculate_consumption_time(url, words_per_minute)

    cache_result("consumo", key, current_time, result)

    if depth > 0:
        with urllib.request.urlopen(str(url)) as response:
            raw_html: str = response.read()

        soup: BeautifulSoup = BeautifulSoup(raw_html, "lxml")
        tags: ResultSet[Tag] = soup("a")

        def recursive(tag: Tag) -> int:
            href: str | AttributeValueList | None = tag.get("href")

            absolute_url: HttpUrl = HttpUrl(urljoin(str(url), href))

            return get_duration(
                absolute_url, words_per_minute=words_per_minute, depth=depth - 1
            )

        result += sum(map(recursive, tags))

    return result


@app.command(
    "url",
    help="Calculate the consumption time of URLs concurrently in a *h *m *s format.",
)
def process_urls(
    urls: Annotated[list[str], typer.Argument()],
    sort: SortOption = DEFAULT_SORT,
    words_per_minute: WordsPerMinuteOption = DEFAULT_WORDS_PER_MINUTE,
    skip_errors: SkipErrorsOption = DEFAULT_SKIP_ERRORS,
    depth: DepthOption = DEFAULT_DEPTH,
) -> None:
    """Calculate the consumption time of URLs concurrently in a *h *m *s format.

    Args:
        urls: A list of URLs pointing to the content whose consumption time
            will be analyzed.
        sort: Whether to sort output in ascending order.
        words_per_minute: Reading speed in words per minute.
        skip_errors: Whether to warn and return 0 in case an exception is raised
            for an URL..
    """

    def duration_resolver(url: str) -> int:
        return get_duration(HttpUrl(url), words_per_minute, depth=depth)

    execute_concurrent_command(
        urls,
        duration_resolver,
        "Processing URL(s)...",
        sort=sort,
        skip_errors=skip_errors,
    )
