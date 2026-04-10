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

from consumo import beautiful_soup_parser
from consumo.cli.cache import cache_result, get_cached_result
from consumo.cli.config import (
    DEFAULT_CACHE,
    DEFAULT_DEPTH,
    DEFAULT_SKIP_ERRORS,
    DEFAULT_SORT,
    DEFAULT_WORDS_PER_MINUTE,
    CacheOption,
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
    is_hosted,
)
from consumo.lib.url import calculate_consumption_time

app: Typer = Typer()


@validate_call
def get_duration(
    url: HttpUrl,
    words_per_minute: NonNegativeInt = 265,
    depth: NonNegativeInt = 0,
    cache: bool = True,
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
        cache: Whether to cache results in a database for later reuse.
            Values are invalidated based on time.

    Returns:
        The time in seconds to consume the content the URL points to.
    """
    if cache:
        try:
            # Not really None, as Pydantic would catch if the URL is malformed
            # before it even reaches this bit of the code.
            normalized_url: str | None = courlan.clean_url(str(url))
            key: str = f"{normalized_url}:{words_per_minute}:{depth}"
            current_time: str = date.today().isoformat()
            cached: int | None = get_cached_result("consumo", key, current_time)

            if cached is not None:
                return cached
        except OperationalError:
            pass

    excluded_hosts: list[str] = ["abc", "AlJazeera", "ant1newsgr", "bbc", "generic"]

    if is_hosted(url, excluded_hosts):
        result: int = get_hosted_multimedia_duration(url)

        if cache:
            cache_result("consumo", key, current_time, result)

        return result

    # Fallback mechanism. First we try to get the duration as if it was
    # a hosted file. If it is not, we calculate the consumption time.
    result: int | None = None

    try:
        result: int = get_multimedia_duration(url)
    except FFmpegError:
        pass

    if result is None:
        result: int = calculate_consumption_time(url, words_per_minute)

    if cache:
        cache_result("consumo", key, current_time, result)

    if depth > 0:
        with urllib.request.urlopen(str(url)) as response:
            raw_html: str = response.read()

        soup: BeautifulSoup = BeautifulSoup(raw_html, beautiful_soup_parser)
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
    cache: CacheOption = DEFAULT_CACHE,
) -> None:
    """Calculate the consumption time of URLs concurrently in a *h *m *s format.

    Args:
        urls: A list of URLs pointing to the content whose consumption time
            will be analyzed.
        sort: Whether to sort output in ascending order.
        words_per_minute: Reading speed in words per minute.
        skip_errors: Whether to warn and return 0 in case an exception is raised
            for an URL.
        depth: How many levels to recursively follow URLs on the page.
        cache: Whether to cache results in a database for later reuse.
            Values are invalidated based on time.
    """

    def duration_resolver(url: str) -> int:
        return get_duration(HttpUrl(url), words_per_minute, depth, cache)

    execute_concurrent_command(
        urls,
        duration_resolver,
        "Processing URL(s)...",
        sort=sort,
        skip_errors=skip_errors,
    )
