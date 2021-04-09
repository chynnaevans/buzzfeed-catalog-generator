from html.parser import HTMLParser
import urllib.request
import json

class CatalogParser(HTMLParser):
    def __init__(self, *args, **kwargs):
        super(CatalogParser, self).__init__(*args, **kwargs)
        self.is_correct_tag = False
        self.json_tag = None
    def handle_starttag(self, tag, attrs):
        if tag == "script" and ('id', '__NEXT_DATA__') in attrs:
            self.is_correct_tag = True
    def handle_data(self, data):
        if self.is_correct_tag:
            self.json_tag = data
            self.is_correct_tag = False

"""
scrape_json: get item data from Buzzfeed shopping page

url: Buzzfeed URL
"""
def scrape_json(url):
    parser = CatalogParser()
    page = urllib.request.urlopen(url)
    content = page.read().decode('utf8')
    page.close()
    parser.feed(content)
    if not json.loads(parser.json_tag):
        print("[FAILED] data not found: ", url)

    return json.loads(parser.json_tag)
