# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
# ]
# ///
"""Command-line interface for the BrowserUse agent."""

import argparse
import os
import sys

# Ensure functions can be imported when running via uv from the root
sys.path.insert(0, os.path.abspath("."))
from functions.browser_use import browser_subagent

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a browser automation task.")
    parser.add_argument("task", help="The task for the browser to perform")
    parser.add_argument("--url", help="Optional starting URL")

    args = parser.parse_args()
    browser_subagent(args.task, args.url)
