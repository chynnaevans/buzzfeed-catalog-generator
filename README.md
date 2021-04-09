## buzzfeed-catalog-generator
The script is designed to extract items from affiliate shopping articles & format them correctly to upload to Facebook catalogs. A CSV file will be generated which should then be uploaded through Commerce Manager.

## Instructions
1. Download folder. Click the green “Code” button and select “Download ZIP”, then unzip in your Downloads folder
![image](https://user-images.githubusercontent.com/27544022/114214917-f2737700-9932-11eb-816b-dafbf65d7206.png)
3. Inside this folder create a CSV file containing the URLs of all the articles you want to use. Format this with one URL per line (this is the default if you save from a Google Sheet)
4. Make sure [Python is downloaded](https://www.python.org/downloads/)
5. Open Terminal and paste the following (these are the packages needed to run the script): `pip3 install pandas && pip3 install urllib`
6. Make sure the folder you downloaded is in your Downloads tab and named “Buzzfeed_Catalog_Script”
7. In terminal, copy and paste the following: `cd Downloads/Buzzfeed_Catalog_Script`
8. In terminal, copy and paste the following: `python3 bulk_buzzfeed_generator.py [NAME OF YOUR CSV HERE]`
    
    a. Eg. if your CSV is named `shopping_urls.csv`: `python3 bulk_buzzfeed_generator.py shopping_urls.csv`
    
    b. The resulting text will tell you how many items have been found and processed in each URL. If you want to suppress this, add to the end of the previous command: `1> /dev/null`
8. Once this is complete, it’ll generate a new CSV named `bulk_catalog_buzzfeed.csv`. Check it over and upload this into your Commerce Manager (Business Manager > Commerce)

## Technical Stuff
### Structure
`./catalog_builder.py` defines a class that finds the JSON containing relevant information (identified by the tag `<script id="__NEXT_DATA__">`). It also defines a function that implements this parser.

`./process_buzzfeed_catalog.py` handles the nuances of your JSON structure. It defines a parser class to process the HTML found inside the JSON & a function that implements this.

`./bulk_buzzfeed_generator.py` implements the parsing functions and allows you to pass in a CSV with multiple article URLs from the command line

`./build_buzzfeed_catalog.py` implements the parsing functions and allowsy you to pass in a single URL from an article

### Possible Extensions
- Use [Commerce API](https://developers.facebook.com/docs/commerce-platform/) to automate the upload
- Have the script write to a Google Doc which can then be set to automatically upload on a cadence (set up done through Commerce Manager)
- Use this script to crawl the Buzzfeed website and automatically find articles
- Find the internal service that creates this JSON blob and implement Commerce API directly (reach out to us and we can help set this up!)

