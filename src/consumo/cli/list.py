# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path
from typing import Annotated

import magic
import typer
from typer import Typer

from consumo.cli.url import process_url
from consumo.lib.cli.core import unsupported_mime_type_error

app: Typer = Typer()


@app.command("list")
def process_list(file: Annotated[Path, typer.Argument()]) -> None:

    if file.is_dir():
        raise IsADirectoryError

    mime_type: str = magic.from_file(str(file), mime=True)

    if mime_type == "text/plain":
        urls: list[str] = file.read_text("utf-8").splitlines()
        # Remove blank lines.
        urls = [url.strip() for url in urls if url.strip()]

        process_url(urls)
    else:
        unsupported_mime_type_error(mime_type)

        raise typer.Exit(1)
