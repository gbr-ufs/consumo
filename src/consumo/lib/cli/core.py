# SPDX-License-Identifier: GPL-3.0-or-later

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
    with ThreadPoolExecutor() as e:
        resolved_durations: Iterator[Second] = e.map(duration_resolver, args)

        return dict(zip(args, resolved_durations))


def execute_concurrent_command(
    args: list[Any],
    resolver: Callable[[Any], Second],
    task_description: str = "Processing...",
) -> None:
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as p:
        p.add_task(task_description, total=None)
        results: dict[Any, Second] = handle_multiple_args(args, resolver)

    if configuration.sort:
        # Sort dictionary by time in ascending order.
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
    print(f"[bold red]Unsupported file type: {mime_type}[/bold red].")
