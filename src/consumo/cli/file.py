# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path
from typing import Annotated, Callable

import magic
import typer
from pydantic import PositiveInt, validate_call
from rich import print
from typer import Typer

from consumo.lib.cli.core import execute_concurrent_command, unsupported_mime_type_error
from consumo.lib.cli.state import configuration
from consumo.lib.file.html import (
    calculate_consumption_time as calculate_html_consumption_time,
)
from consumo.lib.file.image import calculate_viewing_time
from consumo.lib.file.mass_media import (
    calculate_consumption_time as calculate_mass_media_consumption_time,
)
from consumo.lib.file.multimedia import get_duration as get_multimedia_duration
from consumo.lib.file.text import (
    calculate_consumption_time as calculate_text_consumption_time,
)
from consumo.lib.types import Second

app: Typer = Typer()


@validate_call()
def get_duration(file: Path, words_per_minute: PositiveInt) -> Second:

    if file.is_dir():
        raise IsADirectoryError

    mime_type: str = magic.from_file(str(file), mime=True)
    type, subtype = mime_type.split("/", 1)
    multimedia_types = ("audio", "video")

    if type == "image":
        return calculate_viewing_time(1)

    if type in multimedia_types:
        return get_multimedia_duration(file)

    mime_type_handler: dict[str, Callable[[Path, PositiveInt], Second]] = {
        "application/epub+zip": calculate_mass_media_consumption_time,
        "application/pdf": calculate_mass_media_consumption_time,
        "application/x-mobipocket-ebook": calculate_mass_media_consumption_time,
        "text/html": calculate_html_consumption_time,
        "text/plain": calculate_text_consumption_time,
    }

    handler: Callable[[Path, PositiveInt], Second] | None = mime_type_handler.get(
        mime_type
    )

    if handler is None:
        unsupported_mime_type_error(mime_type)

        raise typer.Exit(1)

    return handler(file, words_per_minute)


@app.command("file")
def process_file(
    files: Annotated[list[Path], typer.Argument(exists=True, readable=True)],
) -> None:
    def duration_resolver(file: Path) -> Second:
        return get_duration(file, configuration.words_per_minute)

    try:
        execute_concurrent_command(files, duration_resolver, "Processing files...")
    except IsADirectoryError:
        print("[bold red]Directories are unsupported.[/bold red]")

        raise typer.Exit(1)
