# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Annotated

import typer
from pydantic import PositiveInt
from typer import Typer

from consumo.cli.file import app as file_app
from consumo.cli.list import app as list_app
from consumo.cli.url import app as url_app
from consumo.cli.version import app as version_app
from consumo.lib.cli.state import configuration

app: Typer = Typer()

app.add_typer(file_app)
app.add_typer(list_app)
app.add_typer(version_app)
app.add_typer(url_app)


@app.callback()
def main(
    sort: Annotated[
        bool, typer.Option(help="Sort the output by duration in ascending order.")
    ] = False,
    words_per_minute: Annotated[
        PositiveInt, typer.Option(help="Reading speed in words per minute.")
    ] = 265,
) -> None:
    """Content consumption analyzer CLI."""
    configuration.sort = sort
    configuration.words_per_minute = words_per_minute
