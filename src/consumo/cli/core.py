# SPDX-License-Identifier: GPL-3.0-or-later

"""Core interface and runtime functions for the program."""

from concurrent.futures import Future, ThreadPoolExecutor
from typing import Any, Callable, Iterator

import rich
from rich.progress import Progress, SpinnerColumn, TextColumn

from consumo.lib.formatting import format_time


def exception_warning(argument: Any, exception: Exception) -> None:
    """Print a warning message for an exception.

    Args:
        argument: Original argument that caused the exception.
        exception: The exception caused by the argument.
    """
    message: str = f"{argument} # {exception.__class__.__name__}, {exception.__doc__}"

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
    with ThreadPoolExecutor() as e:
        if skip_errors:
            results: list[int] = []
            arg_exception: dict[Any, Exception] = {}

            for arg in args:
                result: int = 0
                future: Future[int] = e.submit(duration_resolver, arg)

                try:
                    result: int = future.result()
                except Exception as exception:
                    arg_exception[arg] = exception

                results.append(result)

            # This has a pragma to disable test coverage because, for some
            # reason, pytst-cov can't register that
            # `test_process_files_not_a_url_skip_errors` covers this branch.
            # To summarize, consider this branch covered.
            if arg_exception:  # pragma: no cover
                message_warning: str = "Warning: exceptions for some arguments caught, returning 0 for them"

                rich.print(f"[bold yellow]{message_warning}[/bold yellow]")

                for arg, exception in arg_exception.items():
                    exception_warning(arg, exception)

            return dict(zip(args, results))
        else:
            resolved_durations: Iterator[int] = e.map(duration_resolver, args)

            return dict(zip(args, resolved_durations))


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
        results: dict[Any, int] = handle_multiple_args(
            args, duration_resolver, skip_errors=skip_errors
        )

    if sort:
        results: dict[Any, int] = dict(
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
    color: str = "bold red"
    message: str = f"Unsupported MIME type: {mime_type}"

    rich.print(f"[{color}]{message}[/{color}]")
