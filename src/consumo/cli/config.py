# SPDX-License-Identifier: GPL-3.0-or-later

"""Configuration loader module."""

import os
import tomllib
from pathlib import Path
from tomllib import TOMLDecodeError
from typing import Annotated, Any

import rich
import typer
from pydantic import NonNegativeInt


def environment_variable_interpretation_warning(
    environment_variable: str, type: type
) -> None:
    """Print a message warning that an environment variable could not be interpreted as the desired type.

    Args:
        environment_variable: Name of the environment variable.
        type: The type the environment variable should've been interpreted as.
    """
    message: str = f"Could not interpret {environment_variable} as {type.__name__}"

    rich.print(f"[bold yellow]Warning[/bold yellow]: {message}")


def set_default_value(environment_variable: str, value: Any) -> Any:
    """Set the value of a variable based on an environment variable or default.

    Args:
        environment_variable: The environment variable whose value will be
            attempted to be interpreted as one compatible with the variable's
            supposed type.
        value: The fallback value in case the environment variable couldn't be
            correctly interpreted.
    """
    environment_variable_value: Any = os.getenv(environment_variable)

    if environment_variable_value is None:
        return value

    type_cast: type = type(value)

    if type_cast is bool:
        # Words that should be equivalent to True when dealing with booleans.
        truthy_words: tuple = ("true", "1", "yes", "y", "on")

        return environment_variable_value.lower() in truthy_words

    try:
        return type_cast(environment_variable_value)
    except ValueError:
        environment_variable_interpretation_warning(environment_variable, type_cast)
        return value


DEFAULT_SORT: bool = set_default_value("CONSUMO_SORT", False)
DEFAULT_WORDS_PER_MINUTE: NonNegativeInt = set_default_value("CONSUMO_WPM", 265)
DEFAULT_SKIP_ERRORS: bool = set_default_value("CONSUMO_SKIP_ERRORS", False)
DEFAULT_DEPTH: NonNegativeInt = set_default_value("CONSUMO_DEPTH", 0)
DEFAULT_CACHE: bool = set_default_value("CONSUMO_CACHE", True)


SortOption = Annotated[
    bool,
    typer.Option(
        help="Whether to sort the output by duration in ascending order. [env: CONSUMO_SORT=]"
    ),
]
WordsPerMinuteOption = Annotated[
    NonNegativeInt,
    typer.Option(help="Reading speed in words per minute. [env: CONSUMO_WPM=]"),
]
SkipErrorsOption = Annotated[
    bool,
    typer.Option(
        help="Whether to warn and show 0s in case an exception is raised for an item in the list. [env: CONSUMO_SKIP_ERRORS=]"
    ),
]
DepthOption = Annotated[
    NonNegativeInt,
    typer.Option(
        help="How many levels to recursively follow URLs on the page. [env: CONSUMO_DEPTH=]"
    ),
]
CacheOption = Annotated[
    bool,
    typer.Option(
        help="Whether to cache results in a database for later reuse. [env: CONSUMO_CACHE=]"
    ),
]


def configuration_parsing_warning(config_path: Path) -> None:
    """Print a message warning that the configuration file could not be parsed.

    Args:
        config_path: Path to the configuration file.
    """
    message: str = f"Could not parse configuration file at {config_path}"

    rich.print(f"[bold yellow]Warning[/bold yellow]: {message}")


def load_configuration() -> None:
    """Load the program's configuration file."""
    global DEFAULT_SORT
    global DEFAULT_WORDS_PER_MINUTE
    global DEFAULT_SKIP_ERRORS
    global DEFAULT_DEPTH

    app_dir: str = typer.get_app_dir("consumo")
    config_path: Path = Path(app_dir) / "config.toml"

    if config_path.is_file():
        with config_path.open("rb") as c:
            try:
                config_data: dict[str, Any] = tomllib.load(c)
                general: Any = config_data.get("general", {})
                url: Any = config_data.get("url", {})
                key_section_global_type: list[tuple[str, Any, str, type]] = [
                    ("sort", general, "DEFAULT_SORT", bool),
                    ("words_per_minute", general, "DEFAULT_WORDS_PER_MINUTE", int),
                    ("skip_errors", general, "DEFAULT_SKIP_ERRORS", bool),
                    ("cache", url, "DEFAULT_CACHE", bool),
                    ("depth", url, "DEFAULT_DEPTH", int),
                ]

                for (
                    key,
                    section,
                    global_variable_name,
                    type_cast,
                ) in key_section_global_type:
                    if key in section:
                        globals()[global_variable_name] = type_cast(section[key])
            except TOMLDecodeError:
                configuration_parsing_warning(config_path)


load_configuration()
