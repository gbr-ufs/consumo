# SPDX-License-Identifier: GPL-3.0-or-later

"""Configuration loader module."""

import importlib.metadata
import tomllib
from importlib.metadata import PackageMetadata
from pathlib import Path
from tomllib import TOMLDecodeError
from typing import Annotated, Any

import typer
from pydantic import NonNegativeInt, PositiveInt

DEFAULT_SORT: bool = False
DEFAULT_WORDS_PER_MINUTE: NonNegativeInt = 265

SortOption = Annotated[
    bool, typer.Option(help="Sort the output by duration in ascending order.")
]
WordsPerMinuteOption = Annotated[
    NonNegativeInt, typer.Option(help="Reading speed in words per minute.")
]


def configuration_parsing_warning(config_path: Path) -> None:
    """Print a message warning that the configuration filed could not be parsed.

    Args:
        config_path: Path to the configuration file.
    """
    print(
        f"[bold yellow]Could not parse configuration file at {config_path}[/bold yellow]"
    )


def load_configuration() -> None:
    """Load the program's configuration file."""
    global DEFAULT_SORT
    global DEFAULT_WORDS_PER_MINUTE

    metadata: PackageMetadata = importlib.metadata.metadata("consumo")
    name: str = metadata["name"]
    app_dir: str = typer.get_app_dir(name)
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
            except TOMLDecodeError:
                configuration_parsing_warning(config_path)


load_configuration()
