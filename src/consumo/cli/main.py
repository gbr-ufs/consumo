# SPDX-License-Identifier: GPL-3.0-or-later

"""Main program module."""

from typer import Typer

from consumo.cli.file import app as file_app
from consumo.cli.list import app as list_app
from consumo.cli.url import app as url_app
from consumo.cli.version import app as version_app

app: Typer = Typer(no_args_is_help=True, help="Content Consumption Analyzer.")

app.add_typer(file_app)
app.add_typer(list_app)
app.add_typer(version_app)
app.add_typer(url_app)
