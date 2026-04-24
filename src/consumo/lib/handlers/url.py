# SPDX-FileCopyrightText: 2026 Gabriel Santos de Souza <gabriel.santosdesouza@dcomp.ufs.br>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Module for processing URLs."""

import urllib.parse
import urllib.request
from pathlib import Path
from typing import Callable
from urllib.parse import ParseResult

from av.error import FFmpegError
from bs4 import BeautifulSoup, ResultSet, Tag
from bs4.element import AttributeValueList
from pydantic import (
    HttpUrl,
    NonNegativeInt,
    validate_call,
)

from consumo.lib.exceptions import NoCacheError
from consumo.lib.file.multimedia import (
    get_hosted_multimedia_duration,
    get_multimedia_duration,
    is_hosted,
)
from consumo.lib.handlers.core import dummy_cache_resolver, dummy_get_cached_resolver
from consumo.lib.url import calculate_consumption_time


@validate_call
def clean_url(url: HttpUrl) -> HttpUrl:
    """Clean up a URL so it can be used as a cache key.

    Args:
        url: The url that will be cleaned up.

    Returns:
        A clean version of the URL.
    """
    parsed: ParseResult = urllib.parse.urlparse(str(url))
    sorted_query: str = urllib.parse.urlencode(
        sorted(urllib.parse.parse_qsl(parsed.query))
    )
    unparsed: str = urllib.parse.urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path.rstrip("/") or "/",
            parsed.params,
            sorted_query,
            "",
        )
    )

    return HttpUrl(unparsed)


@validate_call
def get_duration(
    url: HttpUrl,
    words_per_minute: NonNegativeInt = 265,
    depth: NonNegativeInt = 0,
    cache: bool = True,
    cache_dir: Path = Path.cwd(),
    get_cached_resolver: Callable[[Path, str], int] = dummy_get_cached_resolver,
    cache_resolver: Callable[[Path, str, int, int], None] = dummy_cache_resolver,
) -> int:
    """Get the duration or calculate the consumption time of a URL in seconds.

    Gets the duration of media from hosting platforms or direct file
    links, and calculates the consumption time otherwise.

    Args:
        url: The URL of the content whose duration or consumption time will be
            analyzed.
        words_per_minute: Reading speed in words per minute.
        depth: How many levels to recursively follow URLs on the page.
        cache: Whether to cache results in a database for later reuse.
            Values are invalidated based on time.
        get_cached_resolver: Function for getting a value from a cache system
            whose signature consists of cache directory, key, and time (date) for
            cache invalidation.
        cache_resolver: Function for storing a value in a cache system  whose
            signature consists of cache directory, key, value, and time (date) for
            cache invalidation.

    !!! warning

        `get_cached_resolver` and `cache_resolver` have dummy default values. You have
        to implement your own cache functions if you want to use cache!

    Returns:
        The time in seconds to consume the content the URL points to.
    """
    # 1 day in seconds.
    time_to_live: int = 86400
    normalized_url: HttpUrl = clean_url(url)
    key: str = f"{normalized_url.unicode_string()}:{words_per_minute}:{depth}"

    if cache:
        try:
            return get_cached_resolver(cache_dir, key)
        except NoCacheError:
            pass

    if is_hosted(url):
        result: int = get_hosted_multimedia_duration(url)

        if cache:
            cache_resolver(cache_dir, key, result, time_to_live)

        return result

    try:
        result: int = get_multimedia_duration(url)
    except FFmpegError:
        result: int = calculate_consumption_time(url, words_per_minute)

    if cache:
        cache_resolver(cache_dir, key, result, time_to_live)

    if depth > 0:
        with urllib.request.urlopen(str(url)) as response:
            raw_html: str = response.read()

        soup: BeautifulSoup = BeautifulSoup(raw_html, "lxml")
        tags: ResultSet[Tag] = soup("a")

        def recursive(tag: Tag) -> int:
            href: str | AttributeValueList | None = tag.get("href")

            absolute_url: HttpUrl = HttpUrl(urllib.parse.urljoin(str(url), href))

            return get_duration(
                absolute_url, words_per_minute=words_per_minute, depth=depth - 1
            )

        result += sum(map(recursive, tags))

    return result
