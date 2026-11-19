"""Pieces shared by the three scripts: command line and where outputs go."""
import argparse
from pathlib import Path

from i18n import LANGUAGES

# Starts with "_" so inventory.py never scans its own outputs.
TOOLS_DIR = "_mlo"


def output_dir(root: Path) -> Path:
    """<root>/_mlo/output: CSVs, plan and move log. Created if missing."""
    path = root / TOOLS_DIR / "output"
    path.mkdir(parents=True, exist_ok=True)
    return path


def parser(description: str) -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=description)
    p.add_argument("root", type=Path, help="music library folder")
    # i18n.py already read --lang from sys.argv; declared here so argparse accepts it
    p.add_argument("--lang", choices=LANGUAGES, help="output language (default: en or MLO_LANG)")
    return p
