# SPDX-License-Identifier: GPL-3.0-or-later

"""Global CLI state management module."""

from typing import Annotated

import typer
from pydantic import PositiveInt
from typer import Typer

from consumo.cli.file import app as file_app
from consumo.cli.list import app as list_app
from consumo.cli.state import configuration
from consumo.cli.url import app as url_app
from consumo.cli.version import app as version_app

app: Typer = Typer()

app.add_typer(file_app)
app.add_typer(list_app)
app.add_typer(version_app)
app.add_typer(url_app)


@app.callback(help="Content consumption analyzer CLI.")
def main(
    sort: Annotated[
        bool, typer.Option(help="Sort the output by duration in ascending order.")
    ] = False,
    words_per_minute: Annotated[
        PositiveInt, typer.Option(help="Reading speed in words per minute.")
    ] = 265,
) -> None:
    """Configure the global state of the application with CLI options.

    Args:
        sort: Whether to sort the output in ascending order before printing.
        words_per_minute: Reading speed in words per minute.
    """
    configuration.sort = sort
    configuration.words_per_minute = words_per_minute
