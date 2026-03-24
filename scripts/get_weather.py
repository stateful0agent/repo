# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
# ]
# ///
import argparse
import requests
import sys


def get_weather(city: str):
    url = f"https://wttr.in/{city}?format=3"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        print(response.text.strip())
    except Exception as e:
        print(f"Error fetching weather: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetch the current weather for a city."
    )
    parser.add_argument(
        "city",
        type=str,
        nargs="?",
        default="",
        help="City to get weather for (default: auto-detect based on IP)",
    )
    args = parser.parse_args()

    get_weather(args.city)
