# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
# ]
# ///
import argparse
import requests
from concurrent.futures import ThreadPoolExecutor


def fetch_story(story_id: int) -> dict:
    url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()


def get_hn_top_stories(limit: int):
    """Fetch top stories from Hacker News concurrently."""
    top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    response = requests.get(top_stories_url)
    response.raise_for_status()
    story_ids = response.json()[:limit]

    with ThreadPoolExecutor(max_workers=min(limit, 10)) as executor:
        stories = list(executor.map(fetch_story, story_ids))

    return stories


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch top stories from Hacker News.")
    parser.add_argument(
        "-n", "--limit", type=int, default=5, help="Number of stories to fetch"
    )
    args = parser.parse_args()

    try:
        stories = get_hn_top_stories(args.limit)
        for i, story in enumerate(stories, 1):
            title = story.get("title", "No Title")
            url = story.get(
                "url", f"https://news.ycombinator.com/item?id={story.get('id')}"
            )
            print(f"{i}. {title}")
            print(f"   {url}")
    except Exception as e:
        print(f"Error fetching stories: {e}")
