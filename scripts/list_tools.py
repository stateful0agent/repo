"""List all python scripts in the repository."""

import argparse
import glob
import os


def list_scripts(directory: str) -> None:
    """Print paths to all python scripts in the directory."""
    paths = glob.glob(os.path.join(directory, "**/*.py"), recursive=True)
    for path in sorted(paths):
        if ".venv" not in path and "site-packages" not in path:
            print(f"Tool found: {path}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="List available python scripts.")
    p.add_argument("--dir", default=".", help="Base directory to search for scripts.")
    args = p.parse_args()
    list_scripts(args.dir)
