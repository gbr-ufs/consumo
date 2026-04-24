# SPDX-FileCopyrightText: 2026 Gabriel Santos de Souza <gabriel.santosdesouza@dcomp.ufs.br>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Configuration loader module."""

import os
import sys
import tomllib
from pathlib import Path
from tomllib import TOMLDecodeError
from typing import Annotated, Any

import rich
import typer
from pydantic import NonNegativeInt


def get_cache_directory(program_name: str) -> Path:
    """Get the program's cache directory on the system.

    Args:
         program_name: The name of the program whose cache path directory will
            be resolved.

    Returns:
         The path to the cache directory of the program on the current system.
    """
    home: Path = Path.home()

    if sys.platform == "darwin":
        return home / "Library" / "Caches" / program_name

    elif sys.platform == "win32":
        local_app_data: str | None = os.getenv("LOCALAPPDATA")

        if local_app_data:
            base_directory: Path = Path(local_app_data)
        else:
            base_directory: Path = home / "AppData" / "Local"
        return base_directory / program_name / "Cache"

    # Unix-like.
    xdg_cache: str | None = os.getenv("XDG_CACHE_HOME")

    if xdg_cache:
        base_directory = Path(xdg_cache)
    else:
        base_directory = home / ".cache"

    return base_directory / program_name


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
DEFAULT_CACHE_DIR: Path = set_default_value(
    "CONSUMO_CACHE_DIR", get_cache_directory("consumo")
)


SortOption = Annotated[
    bool,
    typer.Option(
        default_factory=lambda: DEFAULT_SORT,
        help="Whether to sort the output by duration in ascending order. [env: CONSUMO_SORT=]",
    ),
]
WordsPerMinuteOption = Annotated[
    NonNegativeInt,
    typer.Option(
        default_factory=lambda: DEFAULT_WORDS_PER_MINUTE,
        help="Reading speed in words per minute. [env: CONSUMO_WPM=]",
    ),
]
SkipErrorsOption = Annotated[
    bool,
    typer.Option(
        default_factory=lambda: DEFAULT_SKIP_ERRORS,
        help="Whether to warn and show 0s in case an exception is raised for an item in the list. [env: CONSUMO_SKIP_ERRORS=]",
    ),
]
DepthOption = Annotated[
    NonNegativeInt,
    typer.Option(
        default_factory=lambda: DEFAULT_DEPTH,
        help="How many levels to recursively follow URLs on the page. [env: CONSUMO_DEPTH=]",
    ),
]
CacheOption = Annotated[
    bool,
    typer.Option(
        default_factory=lambda: DEFAULT_CACHE,
        help="Whether to cache results in a database for later reuse. [env: CONSUMO_CACHE=]",
    ),
]
CacheDirOption = Annotated[
    Path,
    typer.Option(
        default_factory=lambda: DEFAULT_CACHE_DIR,
        help="The path to where the cache will be stored. [env: CONSUMO_CACHE_DIR=]",
    ),
]


def configuration_parsing_warning(config_path: Path) -> None:
    """Print a message warning that the configuration file could not be parsed.

    Args:
        config_path: Path to the configuration file.
    """
    message: str = f"Could not parse configuration file at {config_path}"

    rich.print(f"[bold yellow]Warning[/bold yellow]: {message}")


def load_configuration(
    config_file: Path = set_default_value(
        "CONSUMO_CONFIG_FILE", Path(typer.get_app_dir("consumo")) / "config.toml"
    ),
) -> None:
    """Load the program's configuration file."""
    global DEFAULT_SORT
    global DEFAULT_WORDS_PER_MINUTE
    global DEFAULT_SKIP_ERRORS
    global DEFAULT_DEPTH
    global DEFAULT_CACHE
    global DEFAULT_CACHE_DIR

    if config_file.is_file():
        with config_file.open(
            "rb",
        ) as c:
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
                    ("cache_dir", url, "DEFAULT_CACHE_DIR", Path),
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
                configuration_parsing_warning(config_file)
