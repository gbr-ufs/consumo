# SPDX-License-Identifier: GPL-3.0-or-later

"""Core interface and runtime functions for the program."""

from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Iterator

import typer
from rich.progress import Progress, SpinnerColumn, TextColumn

from consumo.lib.formatting import format_time


def exception_warning(argument: Any, exception: Exception) -> None:
    """Print a warning message for an exception.

    Args:
        argument: Original argument that caused the exception.
        exception: The exception caused by the argument.
    """
    message: str = f"{argument} # {exception.__class__.__name__}: {exception}"

    print(message)


def handle_multiple_args(
    args: list[Any], duration_resolver: Callable[[Any], int], skip_errors: bool = False
) -> dict[Any, int]:
    """Get the duration/consumption time of multiple command-line arguments.

    Args:
        args: Command-line arguments.
        duration_resolver: Function used to get the duration/calculate the
            consumption time of the arguments.
        skip_errors: Whether to warn and return 0 in case an exception is raised
            for an argument.

    Returns:
        A dictionary of argument-duration pairs.
    """
    results: dict[Any, int] = {}
    errors: dict[Any, Exception] = {}

    with ThreadPoolExecutor() as e:
        if skip_errors:
            future_to_arg = {e.submit(duration_resolver, arg): arg for arg in args}

            for future in future_to_arg:
                arg = future_to_arg[future]
                try:
                    results[arg] = future.result()
                except Exception as e:
                    errors[arg] = e
                    results[arg] = 0
        else:
            resolved_durations: Iterator[int] = e.map(duration_resolver, args)
            results = dict(zip(args, resolved_durations))

    return results, errors


def execute_concurrent_command(
    args: list[Any],
    duration_resolver: Callable[[Any], int],
    task_description: str = "Processing...",
    sort: bool = False,
    skip_errors: bool = False,
) -> None:
    """Provide a generic interface to process command-line arguments concurrently.

    Args:
        args: Command-line arguments.
        duration_resolver: Function used to get the duration/calculate the consumption
            time of the arguments.
        task_description: Description of what's being done. Generally
            "Processing ARG_TYPE(s)...".
        sort: Whether to sort output in ascending order.
        skip_errors: Whether to warn and return 0 in case an exception is raised
            for an argument.
    """
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as p:
        p.add_task(task_description, total=None)
        results, errors = handle_multiple_args(
            args, duration_resolver, skip_errors=skip_errors
        )

    if sort:
        results: dict[Any, int] = dict(
            sorted(results.items(), key=lambda item: item[1])
        )

    for arg, duration in results.items():
        if skip_errors and errors:
            for arg, exception in errors.items():
                typer.secho(
                    f"{arg} # {exception.__class__.__name__}: {exception}", err=True
                )

        formatted_time: str = format_time(duration)

        if len(results) > 1:
            print(f"{arg} # {formatted_time}")
        else:
            print(formatted_time)
