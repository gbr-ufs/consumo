# SPDX-License-Identifier: GPL-3.0-or-later

"""Core interface and runtime functions for the program."""

from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Iterator

from rich.progress import Progress, SpinnerColumn, TextColumn

from consumo.cli.state import configuration
from consumo.lib.types import Second


def format_time(seconds: int) -> str:
    minutes: int = seconds // 60
    seconds %= 60
    hours: int = (minutes // 60) % 24
    minutes %= 60
    time: str = ""

    if hours:
        time += f"{hours}h "

    if minutes:
        time += f"{minutes}m "

    time += f"{seconds}s"

    return time


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
) -> None:
    """Provide a generic interface to process command-line arguments concurrently.

    Args:
        args: Command-line arguments.
        duration_resolver: Function used to get the duration/calculate the consumption
            time of the arguments.
        task_description: Description of what's being done. Generally
            "Processing ARG_TYPE(s)...".
    """
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as p:
        p.add_task(task_description, total=None)
        results: dict[Any, Second] = handle_multiple_args(args, duration_resolver)

    if configuration.sort:
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
