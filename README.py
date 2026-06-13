from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from pydoc_markdown import main

PRJ_DIR = Path(__file__).resolve().parent

with open(PRJ_DIR.joinpath("README.md"), 'w') as f:
    with redirect_stdout(f): main.cli()