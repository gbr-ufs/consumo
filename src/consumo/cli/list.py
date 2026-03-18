# SPDX-License-Identifier: GPL-3.0-or-later

"""Link list file handler command module."""

from pathlib import Path
from typing import Annotated

import magic
import typer
from typer import Typer

from consumo.cli.config import (
    DEFAULT_SORT,
    DEFAULT_WORDS_PER_MINUTE,
    SortOption,
    WordsPerMinuteOption,
)
from consumo.cli.core import (
    unsupported_mime_type_error,
)
from consumo.cli.url import process_urls

app: Typer = Typer()


@app.command(
    "list",
    help="Calculate the consumption time of all the links in a link list file in a *h *m *s format.",
)
def process_list(
    file: Annotated[Path, typer.Argument()],
    sort: SortOption = DEFAULT_SORT,
    words_per_minute: WordsPerMinuteOption = DEFAULT_WORDS_PER_MINUTE,
) -> None:
    """Calculate the consumption time of all the links in a link list file in a *h *m *s format.

    Args:
        file: The path to the file containing the list of links.
        sort: Whether to sort output in ascending order.
        words_per_minute: Reading speed in words per minute.

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
        IsADirectoryError: If the file path points to a directory.
        typer.Exit: Raised with exit code 1 if the file isn't a plain text file.
    """
    if file.is_dir():
        raise IsADirectoryError

    mime_type: str = magic.from_file(str(file), mime=True)

    if mime_type == "text/plain":
        urls: list[str] = file.read_text("utf-8").splitlines()

        # Filter out empty lines to prevent processing errors.
        urls: list[str] = [url.strip() for url in urls if url.strip()]

        process_urls(urls, sort, words_per_minute)
    else:
        unsupported_mime_type_error(mime_type)

        raise typer.Exit(1)
