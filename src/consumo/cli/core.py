# SPDX-License-Identifier: GPL-3.0-or-later

"""Core interface and runtime functions for the program."""

from concurrent.futures import ThreadPoolExecutor
from typing import Annotated, Any, Callable, Iterator

import typer
from pydantic import PositiveInt
from rich.progress import Progress, SpinnerColumn, TextColumn

from consumo.lib.formatting import format_time
from consumo.lib.types import Second

SortOption = Annotated[
    bool, typer.Option(help="Sort the output by duration in ascending order.")
]
WordsPerMinuteOption = Annotated[
    PositiveInt, typer.Option(help="Reading speed in words per minute.")
]


def handle_multiple_args(
    args: list[Any], duration_resolver: Callable[[Any], Second]
) -> dict[Any, Second]:
    """Get the duration/consumption time of multiple command-line arguments.

    Args:
        args: Command-line arguments.
        duration_resolver: Function used to get the duration/calculate the
            consumption time of the arguments.

    Returns:
        A dictionary of argument-duration pairs.
    """
    with ThreadPoolExecutor() as e:
        resolved_durations: Iterator[Second] = e.map(duration_resolver, args)

        return dict(zip(args, resolved_durations))


def execute_concurrent_command(
    args: list[Any],
    duration_resolver: Callable[[Any], Second],
    task_description: str = "Processing...",
    sort: bool = False,
) -> None:
    """Provide a generic interface to process command-line arguments concurrently.

    Args:
        args: Command-line arguments.
        duration_resolver: Function used to get the duration/calculate the consumption
            time of the arguments.
        task_description: Description of what's being done. Generally
            "Processing ARG_TYPE(s)...".
        sort: Whether to sort output in ascending order.
    """
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as p:
        p.add_task(task_description, total=None)
        results: dict[Any, Second] = handle_multiple_args(args, duration_resolver)

    if sort:
        results: dict[Any, Second] = dict(
            sorted(results.items(), key=lambda item: item[1])
        )

    for arg, duration in results.items():
        formatted_time: str = format_time(duration)

        if len(results) > 1:
            print(f"{arg} # {formatted_time}")
        else:
            print(formatted_time)


def unsupported_mime_type_error(mime_type: str) -> None:
    """Print a message reporting that the file is unsupported.

    Args:
        mime_type: The MIME type of the file.
    """
    print(f"[bold red]Unsupported MIME type: {mime_type}[/bold red].")
