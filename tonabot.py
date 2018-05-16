from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from urllib.parse import urlencode 
import re 

def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)
def log_error(e):
    print(e)

def get_size(string):
    term = r"([0-9]+){1,3}\s?gb"
    m = re.findall(term,string.lower())
    if m:
        return m[0]
    else:
        term_gig = r"([0-9]+){1,3}\s?gig"
        n = re.findall(term_gig,string.lower())
        if n: 
            return n[0]
        else:
            return None

tonaton = "https://tonaton.com"
tonaton_url = "https://tonaton.com/en/ads/ghana/electronics?"

def create_search_url(term,page_no):
    params = {'query': term, 'page' : page_no}
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
    
    size = get_size(descr)

    # Get the size from the string 9       Used              kob    Accra        None  GH₵ 1,000  None                Apple iPhone 7 Plus (Used)  /en/ad/apple-iphone-7-plus-used-for-sale-accra...

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

    date = html.select('.date')[0].text
    return descr, condition, number, vendor, size, date

def confirm(text, rubric):
    if rubric.lower() in text.lower():
        return True
    else:
        return False

def get_ad_details(content):
    title = content.select('.item-title')[0].text
    if confirm(title, ' 7 '):        
        url = content.select('.item-title')[0]['href']
        area = content.select('.item-area')[0].text
        price = content.select('.item-info')[0].text
        item = {'title' : title, 'location': area, 'price': price, 'url': url}
        return item
    else:
        return None


import pandas as pd

def search_page(term, page_no):
    search_url = create_search_url(term, page_no)    
    html = BeautifulSoup(get_page(search_url), 'html.parser')
    ads = html.select(".item-content")
    ads_dict = []
    for content in ads:
        item = get_ad_details(content)
        if(item):
            descr, condition, number, vendor,size,date = inspect_iphone(tonaton + item['url'])
            extras = {'description': descr, 'condition' : condition, 'number' : number, 'dealer' : vendor,'size' : str(size), 'date':date }
            item = {**item, **extras}
            # del item['url']
            del item['description']
            # print(item['title'] + ' - ' + item['price'] + ' - ' + item['condition'] + ' - ' + str(item['dealer']) + ' - ' + item["number"])
            ads_dict.append(item)
    return ads_dict

# print(inspect_iphone("https://tonaton.com/en/ad/apple-iphone-8-plus-256gb-new-for-sale-accra-25"))
def search(term, target_no):
    result = []
    for i in range(1, target_no):
        # print("Page {}".format(i))
        result = result + search_page(term, i)

    stuff = pd.DataFrame(result)
    print(stuff.to_string())
    



# get_size("Brand new iPhone 8 Plus 256gb")
# print(get_size("iPhone  8 plus 256 GB factory  unlocked")

search("iphone 7 plus", 2)



#TODO
# The size part some people use 'gig' instead