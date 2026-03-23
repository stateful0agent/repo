# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
# ]
# ///
import argparse
import requests


def get_hn_top_stories(limit: int):
    """Fetch top stories from Hacker News."""
    top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    response = requests.get(top_stories_url)
    response.raise_for_status()
    story_ids = response.json()[:limit]

    stories = []
    for story_id in story_ids:
        story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        story_resp = requests.get(story_url)
        story_resp.raise_for_status()
        stories.append(story_resp.json())

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
