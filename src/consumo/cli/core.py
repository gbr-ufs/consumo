# SPDX-License-Identifier: GPL-3.0-or-later

"""Core interface and runtime functions for the program."""

from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Iterator

from rich.progress import Progress, SpinnerColumn, TextColumn

from consumo.cli.state import configuration
from consumo.lib.types import Second


def format_time(total_seconds: int) -> str:
    """Format the duration/consumption time given in seconds in a *h *m *s format.

    Args:
        seconds: The duration/consumption time in seconds of the content.

    Returns:
        The duration/consumption time in a *h *m *s format.
    """
    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    hours %= 24

    parts: list[str] = []

    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")

    parts.append(f"{seconds}s")

    return " ".join(parts)


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
