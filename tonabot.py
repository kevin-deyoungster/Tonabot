from requests import get
from bs4 import BeautifulSoup
from pprint import pprint
from datetime import datetime
import threading

TONATON_URL = "https://tonaton.com/en/ads/ghana/electronics"
TONATON_SEARCH_URL = "https://tonaton.com/en/ads/ghana/electronics?query="
TONATON_BASE = "https://tonaton.com"

LAST_CHECKED = datetime.strptime("9 Aug 8:00 pm", "%d %b %I:%M %p")

response = get(TONATON_URL)
html = BeautifulSoup(response.content, 'html.parser')


def get_html_soup(link):
    response = get(link)
    html = BeautifulSoup(response.content, 'html.parser')
    return html


def get_extra_dets(item_url):
    html = get_html_soup(item_url)
    date = html.select(".date")[0].text
    return date


def search_for(item):
    item_search_url = TONATON_SEARCH_URL + item
    html = get_html_soup(item_search_url)

    result_list = html.find("div", {"class": "serp-items"})

    ads = result_list.select(".ui-item")
    ad_dict = []
    for ad in ads:
        ad_title = ad.select(".item-title")[0].text
        ad_price = ad.select(".item-info")[0].text
        ad_url = TONATON_BASE + ad.select(".item-title")[0]["href"]
        ad_date = get_extra_dets(ad_url)
        proper_date = datetime.strptime(ad_date, "%d %b %I:%M %p")

        if proper_date > LAST_CHECKED:
            ad_dict.append(
                {"name": ad_title, "price": ad_price, "date": ad_date, "proper_date": proper_date})

    return ad_dict


from win10toast import ToastNotifier


def show_notifications(heading, text, seconds):
    toaster = ToastNotifier()
    toaster.show_toast(heading, text, duration=3)


def run():
    threading.Timer(120.0, run).start()
    ads = search_for("iphone 8")
    LAST_CHECKED = datetime.now().strftime("%d %b %I:%M %p")
    # Save last checked to a file

    if len(ads) == 0:
        show_notifications("Tonabot!", "No ads found", 2)
    else:
        for ad in ads:
            information = ad["price"] + "\n" + ad["name"]
            show_notifications("Tonabot!", information, 3)


run()
