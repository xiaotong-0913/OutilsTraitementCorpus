import requests
from bs4 import BeautifulSoup
import time

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/119.0.0.0 Safari/537.36"
    )
}
BASE_URL = "https://www.rottentomatoes.com"


BROWSE_PAGES = [
    # New Movies in Theaters
    "https://www.rottentomatoes.com/browse/movies_in_theaters/sort:newest",
    # Movies on Fandango at home
    "https://www.rottentomatoes.com/browse/movies_at_home/affiliates:fandango-at-home",
]

def scrape_movie_links(browse_url, limit=20):
    """
    Retrieve up to `limit` movie detail links from a Browse page.
    Locate <span data-qa="discovery-media-list-item-title"> entries,
    then go up to their parent <a> to get the detail URL.

    """
    resp = requests.get(browse_url, headers=HEADERS)
    soup = BeautifulSoup(resp.text, "html.parser")

    out = []
    # span：data-qa=discovery-media-list-item-title
    for span in soup.find_all("span", {"data-qa": "discovery-media-list-item-title"}):
        a = span.find_parent("a", href=True)
        if not a:
            continue
        href = a["href"]
        
        if not href.startswith("/m/"):
            continue
        full = BASE_URL + href
        if full not in out:
            out.append(full)
        if len(out) >= limit:
            break
    return out

def main():
    for url in BROWSE_PAGES:

        print(f"\n>>> scapping (first {20} links from）: {url}\n")
        links = scrape_movie_links(url, limit=50)
        for link in links:
            print(link)
        
        time.sleep(1)

if __name__ == "__main__":
    main()
