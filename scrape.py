import urllib
from bs4 import BeautifulSoup, SoupStrainer
import urllib.request
from pathlib import Path

# This is the URL to the list of all pages in the Hollow Knight wiki
# with the list being paginated at the entry "Maggot"
BASE_URL_LIST = ['https://hollowknight.fandom.com/wiki/Special:AllPages',
                 'https://hollowknight.fandom.com/wiki/Special:AllPages?from=Maggot']


def get_links(href_set: set[str], url: str):
    """Extract all links from the given url and add them to the set."""
    uf = urllib.request.urlopen(url)
    html = uf.read()
    soup = BeautifulSoup(html, features="html.parser")

    # Get list of all subpages
    links = soup.find("ul", {"class": "mw-allpages-chunk"}).find_all("a")
    for link in links:
        href = link.get("href")
        href_set.add(href)


def scrape_raw(hrefs: list[str]):
    """Scrape the raw text from the given list of links.
    and write them to the output directory.
    """
    for idx, href in enumerate(hrefs):
        try:
            # Fetch HTML content
            uf = urllib.request.urlopen(href)
            html = uf.read()

            # Parse data with BS
            soup = BeautifulSoup(html, features="html.parser")

            # Clean up by removing Javascript and CSS
            for data in soup(['style', 'script']):
                # Remove tags
                data.decompose()

            # Write to output file
            output_dir = 'output-raw/' + \
                href.replace('https://hollowknight.fandom.com/wiki/',
                             '').replace('/', '-')
            with open(output_dir, 'w') as file:
                file.write(soup.prettify())

            # Print out completetion message
            print(f'({idx+1}/{len(hrefs)}) Finished getting text from {href}')
        except:
            print(f'({idx+1}/{len(hrefs)}) ERROR on {href}')


def main():
    """Main entry point of the script."""
    # Create output directory
    Path("output-raw").mkdir(parents=True, exist_ok=True)

    # Get all links
    href_set = set()
    for url in BASE_URL_LIST:
        get_links(href_set, url)

    print(f"Found {len(href_set)} links")

    # Join the base url to the links and remove the Silksong pages
    full_hrefs = ['https://hollowknight.fandom.com' +
                  a for a in list(href_set) if 'Silksong' not in a]

    # Scrape the raw text from the pages and write them to the output directory
    scrape_raw(full_hrefs)


if __name__ == "__main__":
    main()
