from requests import get
from bs4 import BeautifulSoup
from pprint import pprint
from datetime import datetime
import threading

import sys
import subprocess

if sys.platform == 'win32':
    from win10toast import ToastNotifier

# Urls
TONATON_BASE = "https://tonaton.com"
TONATON_URL = "https://tonaton.com/en/ads/ghana/electronics"
TONATON_SEARCH_URL = "https://tonaton.com/en/ads/ghana/electronics?query="


LAST_CHECKED = datetime.strptime("9 Aug 8:00 pm", "%d %b %I:%M %p")

response = get(TONATON_URL)
html = BeautifulSoup(response.content, 'html.parser')


def get_html_soup(link):
    '''
    Accesses url and returns beautifulsoup of the pafe
    '''
    response = get(link)
    html = BeautifulSoup(response.content, 'html.parser')
    return html


def get_extra_dets(item_url):
    '''
    This goes futher into an ads page and extracts extra info
    Currently extracts only date
    '''
    html = get_html_soup(item_url)
    date = html.select(".date")[0].text
    return date


def search_for(item):
    '''
    Main code to handle searching for [item]
    '''
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


def show_notifications(heading, text, seconds):
    '''
    This function shows a desktop notification
    '''
    if sys.platform.lower() == 'linux': # Linux Ubuntu
        subprocess.call(['notify-send', heading, text, '-t', '3'])

    if sys.platform.lower() == 'darwin': # MacOS Mavericks +
        subprocess.call(['osascript', '-e', 
                         'display notification "{0}" with title "{1}"'.format(text, heading)])

    elif sys.platform.lower() == 'win32': # Windows
        toaster = ToastNotifier()
        toaster.show_toast(heading, text, duration=3)


def run(searchTerm, interval):
    '''
    Entry point of the program
    '''
    threading.Timer(interval, run).start()
    ads = search_for(searchTerm)
    LAST_CHECKED = datetime.now().strftime("%d %b %I:%M %p")

    if len(ads) == 0:
        show_notifications("Tonabot!", "No ads found", 2)
    else:
        for ad in ads:
            information = ad["price"] + "\n" + ad["name"]
            show_notifications("Tonabot!", information, 3)


run("iphone 8", 120.0)
