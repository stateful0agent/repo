# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
# ]
# ///
import argparse
import sys
import requests


def get_repo_info(repo_name):
    url = f"https://api.github.com/repos/{repo_name}"
    try:
        response = requests.get(
            url, headers={"Accept": "application/vnd.github.v3+json"}
        )
        response.raise_for_status()
        data = response.json()

        print(f"Repository: {data.get('full_name')}")
        print(f"Description: {data.get('description')}")
        print(f"Stars: {data.get('stargazers_count')}")
        print(f"Forks: {data.get('forks_count')}")
        print(f"Language: {data.get('language')}")
        license_info = data.get("license")
        print(f"License: {license_info.get('name') if license_info else 'None'}")
        print(f"Open Issues: {data.get('open_issues_count')}")

    except requests.exceptions.HTTPError as e:
        if e.response is not None and e.response.status_code == 404:
            print(f"Error: Repository '{repo_name}' not found.")
        else:
            print(f"HTTP Error: {e}")
        sys.exit(1)
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Get information about a GitHub repository."
    )
    parser.add_argument(
        "repo",
        help="Repository name in the format 'owner/repo' (e.g., 'torvalds/linux')",
    )
    args = parser.parse_args()

    get_repo_info(args.repo)


if __name__ == "__main__":
    main()
