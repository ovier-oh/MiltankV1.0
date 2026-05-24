"""Project entry point for the interactive CLI."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from miltank.cli import run


def main() -> None:
    """Run the main command-line workflow."""
    run()


if __name__ == "__main__":
    main()
