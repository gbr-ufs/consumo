# SPDX-License-Identifier: GPL-3.0-or-later

"""Configuration loader module."""

import tomllib
from pathlib import Path
from tomllib import TOMLDecodeError
from typing import Annotated, Any

import rich
import typer
from pydantic import NonNegativeInt

DEFAULT_SORT: bool = False
DEFAULT_WORDS_PER_MINUTE: NonNegativeInt = 265
DEFAULT_SKIP_ERRORS: bool = False

SortOption = Annotated[
    bool,
    typer.Option(help="Whether to sort the output by duration in ascending order."),
]
WordsPerMinuteOption = Annotated[
    NonNegativeInt, typer.Option(help="Reading speed in words per minute.")
]
SkipErrorsOption = Annotated[
    bool,
    typer.Option(
        help="Whether to warn and show 0s in case an exception is raised for an item in the list."
    ),
]


def configuration_parsing_warning(config_path: Path) -> None:
    """Print a message warning that the configuration filed could not be parsed.

    Args:
        config_path: Path to the configuration file.
    """
    rich.print(
        f"[bold yellow]Could not parse configuration file at {config_path}[/bold yellow]"
    )


def load_configuration() -> None:
    """Load the program's configuration file."""
    global DEFAULT_SORT
    global DEFAULT_WORDS_PER_MINUTE
    global DEFAULT_SKIP_ERRORS

    app_dir: str = typer.get_app_dir("consumo")
    config_path: Path = Path(app_dir) / "config.toml"

    if config_path.is_file():
        with config_path.open("rb") as c:
            try:
                config_data: dict[str, Any] = tomllib.load(c)
                general: Any = config_data.get("general", {})

                if "sort" in general:
                    DEFAULT_SORT = bool(general["sort"])
                if "words_per_minute" in general:
                    DEFAULT_WORDS_PER_MINUTE = int(general["words_per_minute"])
                if "skip_errors" in general:
                    DEFAULT_SKIP_ERRORS = bool(general["sort"])
            except TOMLDecodeError:
                configuration_parsing_warning(config_path)


load_configuration()
