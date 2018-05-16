from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from urllib.parse import urlencode 




def is_good_response(resp):
    """
    Returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

tonaton = "https://tonaton.com"
tonaton_url = "https://tonaton.com/en/ads/ghana/electronics?"

def create_search_url(term):
    params = {'query': term}
    return tonaton_url + urlencode(params)

def get_page(url):
    with closing(get(url, stream=True)) as resp:
        if is_good_response(resp):
            return resp.content
        else:
            return None

def inspect_iphone(url):
    html = BeautifulSoup(get_page(url), 'html.parser')
    descr = html.select('.item-description')[0].text
    condition = html.select('.item-properties dd')[0].text
    return descr, condition

def search(term):
    search_url = create_search_url(term)
    
    html = BeautifulSoup(get_page(search_url), 'html.parser')
    ads = html.select(".item-content")
    ads_dict = []
    for content in ads:
        title = content.select('.item-title')[0].text
        url = content.select('.item-title')[0]['href']
        area = content.select('.item-area')[0].text
        price = content.select('.item-info')[0].text
        descr, condition = inspect_iphone(tonaton + url)
        item = {'title' : title, 'location': area, 'price': price, 'url': url, 'description': descr, 'condition' : condition}
        ads_dict.append(item)
    
    for ad in ads_dict:
        print(ad['title'] + ' - ' + ad['price'] + ' - ' + ad['url'] + ' - ' + ad['condition'])

search("iphone 8+")


