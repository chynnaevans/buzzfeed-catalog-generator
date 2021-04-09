import json
from html.parser import HTMLParser
import pandas as pd

# Mapping template fields -> Buzzfeed data struct
data_mappings = {
	"data-vars-link-id": "id",
	"data-vars-product-title": "title",
	"data-vars-price.value": "price",
	"data-vars-price.currency": "currency",
	"data-vars-keywords": "category",
	"data-vars-retailers": "brand",
	"data-vars-product-img": "image_link",
}

# Read Buzzfeed HTML
class SubBuzzParser(HTMLParser):
    def __init__(self, base_url, group_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_data_vars = False
        self.description = ""
        self.row = {
            "id": None,
            "title": None,
            "description": "",
            "availability": "in stock",
            "condition": "new",
            "price": "",
            "link": base_url + "#",
            "image_link": None,
            "brand": None,
            "item_group_id": None,
            "currency": "",
            }
        self.group_id = group_id

    def handle_starttag(self, tag, attrs):
        if tag == "div" and ("class", "subbuzz-anchor") in attrs:
            for attr in attrs:
                if attr[0] == "id":
                    self.row["link"] += attr[1]
        elif tag == "span" and ("class", "js-subbuzz__title-text") in attrs:
            self.is_data_vars = True
        elif tag == "a" and self.is_data_vars:
            for attr in attrs:
                if attr[0] in data_mappings and attr[1] != "":
                    self.row[data_mappings[attr[0]]] = attr[1]
    def handle_endtag(self, tag):
        if tag == "span" and self.is_data_vars:
            self.is_data_vars = False
            ###########################
            ##### POST PROCESSING ######
            ###########################
            if self.row["price"] != "" and  float(self.row["price"]) > 0:
                self.row["price"] = self.row["price"] + " " + self.row["currency"]
            else:
                self.row["price"] = None
            self.row["item_group_id"] = self.group_id
            if self.row["title"] != None and len(self.row["title"]) > 150:
                self.row["title"] = self.row["title"][:146] + "..."

    def handle_data(self, data):
        if self.is_data_vars:
            self.row["description"] += data


"""
process_json: extract the fields required to produce the catalog & process resulting HTML contained in the JSON

data: JSON blob pulled from Buzzfeed site
base_url: the url of this article
output_name: name for the resulting CSV file containing the catalog. This is set to append mode so should be consistent.
group_id: Group ID for Facebook catalog
"""
def process_json(data, base_url, output_name, group_id):
    output = []
    for subbuzz in data['props']['pageProps']['subbuzzData']['subbuzzes']:
        parser = SubBuzzParser(base_url, group_id)
        parser.feed(subbuzz)
        output.append(parser.row)

    pd_output = pd.DataFrame(output)
    pd_output = pd_output.dropna()
    if len(pd_output) > 0:
        pd_output.to_csv(output_name + '.csv', mode="a")
        print("[SUCCESS] found ", len(pd_output), " items: ", base_url)
    else:
        print("[FAILED] data not found: ", base_url)
