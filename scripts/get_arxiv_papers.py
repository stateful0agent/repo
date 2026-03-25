# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
# ]
# ///
import argparse
import requests
import xml.etree.ElementTree as ET
import urllib.parse


def fetch_arxiv_papers(query: str, max_results: int) -> list:
    encoded_query = urllib.parse.quote(query)
    url = f"http://export.arxiv.org/api/query?search_query=all:{encoded_query}&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"
    headers = {"User-Agent": "TheoBot/1.0 (script fetching arxiv metadata)"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    root = ET.fromstring(response.text)
    ns = {"atom": "http://www.w3.org/2005/Atom"}

    papers = []
    for entry in root.findall("atom:entry", ns):
        title_elem = entry.find("atom:title", ns)
        title = (
            title_elem.text.replace("\n", " ").strip()
            if title_elem is not None and title_elem.text
            else "No Title"
        )
        title = " ".join(title.split())

        pub_elem = entry.find("atom:published", ns)
        published = (
            pub_elem.text if pub_elem is not None and pub_elem.text else "Unknown Date"
        )

        link_elem = entry.find("atom:id", ns)
        link = link_elem.text if link_elem is not None and link_elem.text else "No Link"

        authors = []
        for author in entry.findall("atom:author", ns):
            name_elem = author.find("atom:name", ns)
            if name_elem is not None and name_elem.text:
                authors.append(name_elem.text)

        papers.append(
            {"title": title, "published": published, "authors": authors, "link": link}
        )
    return papers


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch latest papers from arXiv.")
    parser.add_argument(
        "query", type=str, help="Search query (e.g., 'machine learning')"
    )
    parser.add_argument(
        "-n", "--limit", type=int, default=5, help="Number of papers to fetch"
    )
    args = parser.parse_args()

    try:
        papers = fetch_arxiv_papers(args.query, args.limit)
        if not papers:
            print("No papers found.")
        for i, paper in enumerate(papers, 1):
            authors_str = ", ".join(paper["authors"])
            print(f"{i}. {paper['title']}")
            print(f"   Authors: {authors_str}")
            print(f"   Published: {paper['published']}")
            print(f"   Link: {paper['link']}\n")
    except Exception as e:
        print(f"Error fetching papers: {e}")
