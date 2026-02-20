# SPDX-License-Identifier: GPL-3.0-or-later

from typer import Typer

from consumo.__init__ import __version__

app: Typer = Typer()


@app.command()
def version() -> None:
    print(__version__)
