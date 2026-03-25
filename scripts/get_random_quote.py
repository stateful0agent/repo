# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
# ]
# ///
import argparse
import requests
import sys


def get_quote():
    url = "https://dummyjson.com/quotes/random"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        print(f'\n"{data.get("quote")}"')
        print(f"  - {data.get('author')}\n")
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch quote: {e}")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch a random quote.")
    args = parser.parse_args()
    get_quote()
