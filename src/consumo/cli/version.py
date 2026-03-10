# SPDX-License-Identifier: GPL-3.0-or-later

"""Version information command module."""

from typer import Typer

from consumo.__init__ import __version__

app: Typer = Typer()


@app.command()
def version() -> None:
    """Print the program's version and exit."""
    print(__version__)
