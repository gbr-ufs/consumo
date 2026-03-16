import os
from zipfile import ZipFile, ZIP_DEFLATED

EXE_PATH: str = os.getenv("EXE_PATH")
ZIP_NAME: str = os.getenv("ZIP_NAME")

with ZipFile(ZIP_NAME, "w", ZIP_DEFLATED) as z:
    z.write(EXE_PATH)
    z.write("README.md")
    z.write("LICENSE")
