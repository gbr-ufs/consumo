# SPDX-License-Identifier: GPL-3.0-or-later

"""Main program module."""

import importlib.metadata
from importlib.metadata import PackageMetadata
from typing import Annotated

import typer
from typer import Typer

from consumo.cli.file import app as file_app
from consumo.cli.list import app as list_app
from consumo.cli.url import app as url_app

app: Typer = Typer(no_args_is_help=True, help="Content Consumption Analyzer.")

app.add_typer(file_app)
app.add_typer(list_app)
app.add_typer(url_app)


def version_callback(value: bool) -> None:
    """Print the program's version and exit.

    Args:
        value: Whether to print the program's version.

    Raises:
        typer.Exit: Raised if printing the program's version.
    """
    if value:
        metadata: PackageMetadata = importlib.metadata.metadata("consumo")
        name: str = metadata["name"]
        version: str = metadata["version"]

        print(f"{name} {version}")

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
        version: Whether to print the program's version and exit.
    """
