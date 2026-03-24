# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
# ]
# ///
import argparse
import os
import requests
from concurrent.futures import ThreadPoolExecutor


def fetch_story(story_id: int) -> dict:
    url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()


def get_hn_top_stories(limit: int):
    top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    response = requests.get(top_stories_url)
    response.raise_for_status()
    story_ids = response.json()[:limit]

    with ThreadPoolExecutor(max_workers=min(limit, 10)) as executor:
        stories = list(executor.map(fetch_story, story_ids))

    return stories


def summarize_stories(stories):
    prompt_text = "Summarize the following top stories from Hacker News:\n\n"
    for i, story in enumerate(stories, 1):
        prompt_text += (
            f"{i}. {story.get('title', 'No Title')} (URL: {story.get('url', '')})\n"
        )

    prompt_text += "\nProvide a brief summary of what's trending based on these titles in a couple sentences."

    url = "https://ai-gateway.vercel.sh/v1/chat/completions"
    api_key = os.environ.get("AI_GATEWAY_API_KEY")
    if not api_key:
        raise ValueError("AI_GATEWAY_API_KEY environment variable not set")

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt_text}],
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get Hacker News top stories and summarize them."
    )
    parser.add_argument(
        "-n",
        "--limit",
        type=int,
        default=5,
        help="Number of stories to fetch and summarize",
    )
    args = parser.parse_args()

    try:
        print(f"Fetching top {args.limit} stories...")
        stories = get_hn_top_stories(args.limit)
        print("Summarizing with LLM...")
        summary = summarize_stories(stories)
        print("\n--- HN SUMMARY ---")
        print(summary)
    except Exception as e:
        print(f"Error: {e}")
