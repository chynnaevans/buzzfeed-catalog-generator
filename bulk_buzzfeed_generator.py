"""
To use: `python3 bulk_buzzfeed_generator.py [PASTE CSV NAME HERE]
"""
from catalog_builder import scrape_json
from process_buzzfeed_catalog import process_json
import sys
import csv
from re import match, search

file_name = "buzzfeed_catalog_bulk"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please input one file path")
    else:
        try:
            with open(sys.argv[1], "r") as urlfile:
                urlreader = csv.reader(urlfile)
                for url in urlreader:
                    try:
                        group_id = search(".*buzzfeed\.com\/([a-z0-9\_]+\/[a-z\-0-9]+).*", url[0]).group(1)
                        catalog_json = scrape_json(url[0])
                        process_json(catalog_json, url[0], file_name, group_id)
                    except:
                        print("[SKIPPED]: ", url[0])

        except:
            print("INVALID FILE PATH")
