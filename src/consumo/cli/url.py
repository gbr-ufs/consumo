# SPDX-FileCopyrightText: 2026 Gabriel Santos de Souza <gabriel.santosdesouza@dcomp.ufs.br>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""URL handler command module."""

from typing import Annotated

import typer
from pydantic import (
    HttpUrl,
)
from typer import Typer

from consumo.cli.config import (
    CacheDirOption,
    CacheOption,
    DepthOption,
    SkipErrorsOption,
    SortOption,
    WordsPerMinuteOption,
)
from consumo.cli.core import (
    execute_concurrent_command,
)
from consumo.lib.handlers.url import get_duration

app: Typer = Typer(no_args_is_help=True)


@app.command(
    "url",
    help="Calculate the consumption time of URLs concurrently in a *h *m *s format.",
)
def process_urls(
    urls: Annotated[list[str], typer.Argument()],
    sort: SortOption,
    words_per_minute: WordsPerMinuteOption,
    skip_errors: SkipErrorsOption,
    depth: DepthOption,
    cache: CacheOption,
    cache_dir: CacheDirOption,
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
        cache_dir: The path to where the cache will be stored.
    """

    def duration_resolver(url: str) -> int:
        return get_duration(HttpUrl(url), words_per_minute, depth, cache, cache_dir)

    execute_concurrent_command(
        urls, duration_resolver, "Processing URL(s)...", sort, skip_errors
    )
