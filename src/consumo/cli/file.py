# SPDX-FileCopyrightText: 2026 Gabriel Santos de Souza <gabriel.santosdesouza@dcomp.ufs.br>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""File handler command module."""

from pathlib import Path
from typing import Annotated

import typer
from typer import Typer

from consumo.cli.config import (
    DEFAULT_SKIP_ERRORS,
    DEFAULT_SORT,
    DEFAULT_WORDS_PER_MINUTE,
    SkipErrorsOption,
    SortOption,
    WordsPerMinuteOption,
)
from consumo.cli.core import (
    execute_concurrent_command,
)
from consumo.lib.handlers.file import get_duration

app: Typer = Typer()


@app.command(
    "file",
    help="Calculate the consumption time of files concurrently in a *h *m *s format.",
)
def process_files(
    files: Annotated[list[Path], typer.Argument(dir_okay=False, exists=True)],
    sort: SortOption = DEFAULT_SORT,
    words_per_minute: WordsPerMinuteOption = DEFAULT_WORDS_PER_MINUTE,
    skip_errors: SkipErrorsOption = DEFAULT_SKIP_ERRORS,
) -> None:
    """Calculate the consumption time of files concurrently in a *h *m *s format.

    Args:
        files: The paths to one or multiple files whose consumption time will be
            analyzed.
        sort: Whether to sort output in ascending order.
        words_per_minute: Reading speed in words per minute.
        skip_errors: Whether to warn and return 0 in case an exception is raised
            for a file.
    """

    def duration_resolver(file: Path) -> int:
        return get_duration(
            file,
            words_per_minute,
        )

    execute_concurrent_command(
        files,
        duration_resolver,
        "Processing file(s)...",
        sort=sort,
        skip_errors=skip_errors,
    )
