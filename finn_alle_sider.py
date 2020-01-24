import requests
import urllib3
import sys
import json

from bs4 import BeautifulSoup as BS


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_sitemap() -> BS:
    sitemaps = ["https://www.obos.no/sitemaps/sitemap_obos.no.xml", "http://www.obos.no/sitemap.xml","https://bank.obos.no/sitemap.xml"]
    sitemap=""
    for i in sitemaps:
        tekst = requests.get(i,verify=False).text
        sitemap+=tekst
    return BS(sitemap, "xml")

def find_urlfragment(tag: str, sitemap: BS) -> list:
    locs = sitemap.findAll("loc")
    if tag == "":
        urls = [url.text for url in locs]
    else:
        urls = [url.text for url in locs if tag.lower() in url.text.lower()]
    return urls


if __name__ == "__main__":
    if not sys.argv[1]:
        print("Add a url fragment ex: /bedrift ")
        
    else:
        url = sys.argv [1]

        urls = find_urlfragment(url, get_sitemap())
        with open(f"{url}.json", "w") as file:
            json.dump(urls, file)
        print(f"urler lagret som {url}.json")
