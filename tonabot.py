from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from urllib.parse import urlencode 




def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)
def log_error(e):
    print(e)

tonaton = "https://tonaton.com"
tonaton_url = "https://tonaton.com/en/ads/ghana/electronics?"

def create_search_url(term):
    params = {'query': term}
    return tonaton_url + urlencode(params)

def get_page(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def inspect_iphone(url):
    html = BeautifulSoup(get_page(url), 'html.parser')
    descr = html.select('.item-description')[0].text
    condition = html.select('.item-properties dd')[0].text
    if html.select('.clearfix') is None:
        number = 'None' 
    else:
        if len(html.select('.clearfix')) == 0:
            number = 'None'
        else:
            number = html.select('.clearfix')[0].text

    # print(html.select('.poster a'))
    if html.select('.poster a') is None:
        vendor =  html.select('.poster')[0].text.split("by")[1]
    else:
        if len(html.select('.poster a')) == 0:
            vendor =  html.select('.poster')[0].text.split("by")[1]
        else:
            vendor = html.select('.poster a')[0].text
    return descr, condition, number, vendor

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
        descr, condition, number, vendor = inspect_iphone(tonaton + url)
        item = {'title' : title, 'location': area, 'price': price, 'url': url, 'description': descr, 'condition' : condition, 'number' : number, 'dealer' : vendor}
        print(item['title'] + ' - ' + item['price'] + ' - ' + item['url'] + ' - ' + item['condition'] + ' - ' + str(item['dealer']) + ' - ' + item["number"])
        ads_dict.append(item)

# print(inspect_iphone("https://tonaton.com/en/ad/apple-iphone-8-plus-256gb-new-for-sale-accra-25"))
search("iphone 8+")


