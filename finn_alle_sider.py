import requests
import urllib3
import sys
import json

from bs4 import BeautifulSoup as BS


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_sitemap_obos() -> BS:
    sitemaps = [
        "https://www.obos.no/sitemaps/sitemap_obos.no.xml",
        "http://www.obos.no/sitemap.xml",
        "https://bank.obos.no/sitemap.xml",
    ]
    sitemap = ""
    for i in sitemaps:
        tekst = requests.get(i, verify=False).text
        sitemap += tekst
    return BS(sitemap, "xml")

def get_sitemap_nye() -> BS:
    sitemaps = BS(requests.get("https://nye.obos.no/sitemap.xml", verify=False).text, "lxml")
    sitemaps = sitemaps.findAll("loc")
    sitemap = ""
    for url in sitemaps:
        sitemap += requests.get(url.text, verify=False).text
    return BS(sitemap,"lxml")

def get_all_sitemaps() -> BS:
    nye = get_sitemap_nye()
    obos = get_sitemap_obos()
    nye.urlset.insert(-1,obos.urlset)
    return nye

def find_urlfragment(tag: str, sitemap: BS) -> list:
    locs = sitemap.findAll("loc")
    if tag == "":
        urls = [url.text for url in locs]
    else:
        urls = [url.text for url in locs if tag.lower() in url.text.lower()]
    return urls


def get_titles(urls: list):
    titles = []
    for url in urls:
        response = requests.get(url)
        soup = BS(response.text)
        titles.append(soup.title.text)
    return titles


def get_title(soup: BS):
    try:
        return soup.title.text
    except Exception:
        return "No title found"


if __name__ == "__main__":
    if not sys.argv[1]:
        print("Add a url fragment ex: /bedrift ")

    else:
        url = sys.argv[1]

        urls = find_urlfragment(url, get_sitemap())
        with open(f"{url}.json", "w") as file:
            json.dump(urls, file)
        print(f"urler lagret som {url}.json")
