# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
# ]
# ///

import argparse
import requests
import sys


def get_wikipedia_summary(query: str, lang: str = "en") -> str:
    # Use the Wikipedia REST API for page summaries
    url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{query}"
    try:
        response = requests.get(url, headers={"User-Agent": "Theo-Agent/1.0"})
        response.raise_for_status()
        data = response.json()
        if "extract" in data:
            return data["extract"]
        return "No summary found for this query."
    except requests.exceptions.HTTPError as e:
        if e.response is not None and e.response.status_code == 404:
            return f"Error: Page '{query}' not found."
        return f"HTTP error occurred: {e}"
    except Exception as e:
        return f"An error occurred: {e}"


def main():
    parser = argparse.ArgumentParser(
        description="Fetch Wikipedia summary for a given topic."
    )
    parser.add_argument("query", help="The topic to search for on Wikipedia")
    parser.add_argument(
        "-l", "--lang", default="en", help="Language code (default: en)"
    )
    args = parser.parse_args()

    summary = get_wikipedia_summary(args.query, args.lang)
    print(summary)


if __name__ == "__main__":
    main()
