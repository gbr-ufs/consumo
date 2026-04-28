# SPDX-FileCopyrightText: 2026 Gabriel Santos de Souza <gabriel.santosdesouza@dcomp.ufs.br>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Main program module."""

import importlib.metadata
import sys
from importlib.metadata import PackageMetadata
from typing import Annotated

import typer
from pydantic import ValidationError
from rich.console import Console
from rich.panel import Panel
from typer import Typer

from consumo import MissingMetadataError
from consumo.cli.file import app as file_app
from consumo.cli.list import app as list_app
from consumo.cli.url import app as url_app
from consumo.lib.exceptions import UnsupportedMIMETypeError

app: Typer = Typer(
    no_args_is_help=True,
    help="Content Consumption Analyzer.",
    pretty_exceptions_enable=False,
)

app.add_typer(file_app)
app.add_typer(list_app)
app.add_typer(url_app)


def version_callback(value: bool) -> None:
    """Print the program's version and exit.

    Args:
        value: Whether to print the program's version.

    Raises:
        typer.Exit: When printing the program's version.
    """
    if value:
        metadata: PackageMetadata = importlib.metadata.metadata("consumo")
        version: str = metadata["version"]

        print(f"consumo {version}")

        raise typer.Exit()


@app.callback(help="Content Consumption Analyzer.")
def main(
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            callback=version_callback,
            help="Print the program's version and exit.",
            is_eager=True,
        ),
    ] = False,
) -> None:
    """Arguments and options of the main program.

    Args:
        config_file: Set the configuration file of the program.
        version: Whether to print the program's version and exit.
    """


def run() -> None:
    """Wrapper for `app` to handle exceptions."""
    exceptions = (
        ConnectionError,
        MissingMetadataError,
        UnsupportedMIMETypeError,
        ValidationError,
    )

    try:
        app()
    except exceptions as e:
        error_console: Console = Console(stderr=True)

        error_console.print(
            Panel(
                f"[red]{e.__class__.__name__}:[/red] {e}",
                border_style="red",
                title="Error",
                title_align="left",
            )
        )

        sys.exit(1)
