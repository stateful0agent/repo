# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
# ]
# ///
import argparse
import requests
import sys


def get_joke(category="Programming"):
    url = f"https://v2.jokeapi.dev/joke/{category}?type=single,twopart"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("error"):
            print(f"Error: {data.get('message')}")
            sys.exit(1)

        print(f"\n[{data.get('category')} Joke]")
        if data.get("type") == "single":
            print(f"  {data.get('joke')}")
        else:
            print(f"  {data.get('setup')}")
            print(f"  {data.get('delivery')}")
        print()

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch joke: {e}")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch a random programming joke.")
    parser.add_argument(
        "--category",
        type=str,
        default="Programming",
        help="Joke category (Programming, Misc, Dark, Pun, Spooky, Christmas)",
    )
    args = parser.parse_args()

    get_joke(args.category)
