from bs4 import BeautifulSoup, SoupStrainer
from pathlib import Path
import re
import os


def parse_text(file):
    """Parse the HTML from the given file, extract the text, clean it a bit, and write it to the output directory."""
    try:
        # Extract the text from the file and parse with bs
        html = '\n'.join(file.readlines())
        soup = BeautifulSoup(html, features="html.parser")

        # Start string for current document
        s = ""

        # Get the page title
        page_title = soup.find("h1", {"id": "firstHeading"}).get_text().strip()
        s += f'[{page_title}]. '

        # Get the infobox, if any
        info_box = soup.find("aside", {"class": "portable-infobox"})
        if info_box is not None:
            # Append the info and remove from the body
            s += re.sub('\s+', ' ', info_box.get_text().strip()) + '. '
            info_box.decompose()

        # Remove the hidden table of contents
        toc = soup.find("div", {"id": "toc"})
        if toc is not None:
            toc.decompose()

        # Extract the main text body
        body = soup.find("div", {"class": "mw-parser-output"})
        s += re.sub('Compendium.*$', '', re.sub('\s+',
                    ' ', body.get_text().strip()) + '. ')

        # Remove the text that is in brackets
        s = re.sub('\[.*?\]', '', s)

        # Remove nonstandard text and replace with a period (not in ASCII range 32 to 126)
        s = re.sub('[^ -~]', '.', s)

        # Write to output file
        output_dir = file.name.replace('output-raw', 'output-data')
        with open(output_dir, 'w') as file:
            file.write(s)

        print(f'Finished parsing text from {file.name}')
    except Exception as e:
        print(f'ERROR parsing {file.name}: {e}')


def main():
    """Main entry point of the script."""
    # Create output directory
    Path("output-data").mkdir(parents=True, exist_ok=True)

    # Loop through all files in the output-raw directory
    for filename in os.listdir('output-raw'):
        with open('output-raw/' + filename) as file:
            parse_text(file)


if __name__ == "__main__":
    main()
