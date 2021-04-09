"""
To use: `python3 build_buzzfeed_catalog.py [PASTE ARTICLE URL HERE]
"""
from catalog_builder import scrape_json
from process_buzzfeed_catalog import process_json
import sys
from re import match, search

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please input a single URL")
    elif match(".*buzzfeed\.com\/([a-z0-9\_]+\/[a-z\-0-9]+).*", sys.argv[1]):
        url = sys.argv[1]
        group_id = search(".*buzzfeed\.com\/([a-z0-9\_]+\/[a-z\-0-9]+).*", url).group(1)
        file_name = "buzzfeed_catalog"
        catalog_json = scrape_json(url)
        process_json(catalog_json, url, file_name, group_id)
    else:
        print("No")
