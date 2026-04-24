# SPDX-FileCopyrightText: 2026 Gabriel Santos de Souza <gabriel.santosdesouza@dcomp.ufs.br>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Script for distributing the program with pyinstaller.

I don't recommend running this, just leave it to CI instead.
"""

import os
from zipfile import ZIP_DEFLATED, ZipFile

EXE_PATH: str | None = os.getenv("EXE_PATH")
ZIP_NAME: str | None = os.getenv("ZIP_NAME")

if EXE_PATH is None:
    raise ValueError("EXE_PATH not set")

if ZIP_NAME is None:
    raise ValueError("ZIP_NAME is not set")

with ZipFile(ZIP_NAME, "w", ZIP_DEFLATED) as z:
    z.write(EXE_PATH)
    z.write("README.md")
    z.write("LICENSES/GPL-3.0-or-later.txt")
