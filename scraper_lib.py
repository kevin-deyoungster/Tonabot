"""
This module handles scraping information off the tonaton website
"""

from requests import get
from datetime import datetime
from bs4 import BeautifulSoup

# URLS for the Tonaton Website
TONATON_BASE = "https://tonaton.com"
TONATON_URL = "https://tonaton.com/en/ads/ghana/electronics"
TONATON_SEARCH_URL = "https://tonaton.com/en/ads/ghana/electronics?query="


def get_html_soup(page_url):
    """
    Returns BeautifulSoup of a page 

    Parameters:
    page_url (str): The url of the page 
    """
    response = get(page_url)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup


def get_extra_dets(item_url):
    """
    Goes further into a specific ad page and extracts more info

    Parameters:
    item_url (str): The url of a product page
    """

    # Currently extracts only date, can take more info
    html = get_html_soup(item_url)
    date = html.select(".date")[0].text
    return {"date": date}


def search_for(product_name, last_checked, title_filter=None):
    """
    Scrapes ads for a product from the search results 

    Parameters:
    product_name (str): The name of the product to search for 
    last_checked (datetime): The time of last searching

    Returns: array of ad objects
    """
    ad_results = []

    print(f"Checking for new ads for [ {product_name} ]")
    product_search_url = TONATON_SEARCH_URL + product_name
    html_soup = get_html_soup(product_search_url)

    result_list = html_soup.find("div", {"class": "serp-items"})
    ads = result_list.select(".ui-item")

    for ad in ads:
        ad_title = ad.select(".item-title")[0].text
        ad_price = ad.select(".item-info")[0].text
        ad_url = TONATON_BASE + ad.select(".item-title")[0]["href"]
        ad_details = get_extra_dets(ad_url)
        ad_date = ad_details["date"]
        proper_date = datetime.strptime(ad_date, "%d %b %I:%M %p").replace(
            year=datetime.now().year
        )

        if proper_date > last_checked:

            ad_object = {
                "name": ad_title,
                "price": ad_price,
                "date": ad_date,
                "proper_date": proper_date,
            }

            if title_filter:
                if title_filter in ad_title.lower():
                    ad_results.append(ad_object)
            else:
                ad_results.append(ad_object)

    return ad_results
