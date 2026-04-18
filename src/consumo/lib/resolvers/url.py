# SPDX-License-Identifier: GPL-3.0-or-later

"""Module for processing URLs."""

import urllib.request
from datetime import date
from typing import Any, Callable
from urllib.parse import urljoin

import courlan
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
from consumo.lib.resolvers.core import dummy_cache_resolver, dummy_get_cached_resolver
from consumo.lib.url import calculate_consumption_time


@validate_call
def get_duration(
    url: HttpUrl,
    words_per_minute: NonNegativeInt = 265,
    depth: NonNegativeInt = 0,
    cache: bool = True,
    get_cached_resolver: Callable[[str, str, Any], int] = dummy_get_cached_resolver,
    cache_resolver: Callable[[str, str, int, Any], None] = dummy_cache_resolver,
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
            whose signature consists of program name, key, and time (date) for
            cache invalidation.
        cache_resolver: Function for storing a value in a cache system  whose
            signature consists of program name, key, value, and time (date) for
            cache invalidation.

    !!! warning

        `get_cached_resolver` and `cache_resolver` have dummy default values. You have
        to implement your own cache functions if you want to use cache!

    Returns:
        The time in seconds to consume the content the URL points to.
    """
    if cache:
        try:
            # Not really None, as Pydantic would catch if the URL is malformed
            # before it even reaches this bit of the code.
            normalized_url: str = courlan.clean_url(str(url))  # ty:ignore[invalid-assignment]
            key: str = f"{normalized_url}:{words_per_minute}:{depth}"
            current_time: str = date.today().isoformat()
            cached: int = get_cached_resolver("consumo", key, current_time)

            return cached
        except NoCacheError:
            pass

    if is_hosted(url):
        result: int = get_hosted_multimedia_duration(url)

        if cache:
            cache_resolver("consumo", key, result, current_time)

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
        cache_resolver("consumo", key, result, current_time)

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
