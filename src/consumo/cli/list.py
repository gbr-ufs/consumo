# SPDX-FileCopyrightText: 2026 Gabriel Santos de Souza <gabriel.santosdesouza@dcomp.ufs.br>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Link list file handler command module."""

from pathlib import Path
from typing import Annotated

import magic
import typer
from typer import Typer

from consumo.cli.config import (
    DEFAULT_CACHE,
    DEFAULT_CACHE_DIR,
    DEFAULT_DEPTH,
    DEFAULT_SKIP_ERRORS,
    DEFAULT_SORT,
    DEFAULT_WORDS_PER_MINUTE,
    CacheOption,
    CacheDirOption,
    DepthOption,
    SkipErrorsOption,
    SortOption,
    WordsPerMinuteOption,
)
from consumo.cli.url import process_urls
from consumo.lib.exceptions import UnsupportedMIMETypeError

app: Typer = Typer()


@app.command(
    "list",
    help="Calculate the consumption time of all the links in a link list file in a *h *m *s format.",
)
def process_list(
    file: Annotated[Path, typer.Argument(dir_okay=False, exists=True)],
    sort: SortOption = DEFAULT_SORT,
    words_per_minute: WordsPerMinuteOption = DEFAULT_WORDS_PER_MINUTE,
    skip_errors: SkipErrorsOption = DEFAULT_SKIP_ERRORS,
    depth: DepthOption = DEFAULT_DEPTH,
    cache: CacheOption = DEFAULT_CACHE,
    cache_dir: CacheDirOption = DEFAULT_CACHE_DIR,
) -> None:
    """Calculate the consumption time of all the links in a link list file in a *h *m *s format.

    Args:
        file: The path to the file containing the list of links.
        sort: Whether to sort output in ascending order.
        words_per_minute: Reading speed in words per minute.
        skip_errors: Whether to warn and return 0 in case an exception is raised
            for an item in the list.
        depth: How many levels to recursively follow URLs on the page.
        cache: Whether to cache results in a database for later reuse.
        cache_dir: The path to where the cache will be stored.

    Example:
        A "file with a list of links" is a plain text file that looks like this:

        ```text
        https://en.wikipedia.org/wiki/Python_(programming_language)
        https://en.wikipedia.org/wiki/High-level_programming_language
        https://en.wikipedia.org/wiki/General-purpose_programming_language
        https://en.wikipedia.org/wiki/Code_readability
        https://en.wikipedia.org/wiki/Significant_indentation
        https://en.wikipedia.org/wiki/Type_system#DYNAMIC
        https://en.wikipedia.org/wiki/Garbage_collection_(computer_science)
        https://en.wikipedia.org/wiki/Programming_paradigm
        https://en.wikipedia.org/wiki/Structured_programming
        https://en.wikipedia.org/wiki/Procedural_programming
        https://en.wikipedia.org/wiki/Object-oriented_programming
        https://en.wikipedia.org/wiki/Functional_programming
        ...
        ```

    Raises:
        UnsupportedMIMETypeError: When the file isn't a plain text file.
    """
    mime_type: str = magic.from_file(str(file), mime=True)

    if mime_type == "text/plain":
        urls: list[str] = file.read_text("utf-8").splitlines()

        urls: list[str] = [url.strip() for url in urls if url.strip()]

        process_urls(urls, sort, words_per_minute, skip_errors, depth, cache, cache_dir)
    else:
        raise UnsupportedMIMETypeError("Not a plain text file")
