"""List all python scripts and their descriptions."""

import argparse, ast, glob, os


def get_desc(path: str) -> str:
    try:
        n = ast.parse(open(path, encoding="utf-8").read())
        d = ast.get_docstring(n)
        return d.split("\n")[0] if d else "No description"
    except Exception:
        return "Could not parse"


def list_scripts(d: str) -> None:
    for p in sorted(glob.glob(os.path.join(d, "**/*.py"), recursive=True)):
        if ".venv" not in p and "site-packages" not in p:
            print(f"- {p}: {get_desc(p)}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="List available python scripts.")
    p.add_argument("--dir", default=".", help="Base directory")
    list_scripts(p.parse_args().dir)
