import requests
import json
import pprint
from bs4 import BeautifulSoup
from GmailAPI.SendEmail import format_message, email
from GmailAPI import Service
import time
from lxml.html import fromstring
from itertools import cycle
from random import choice
import traceback

PROXIES = {'https': '162.144.92.212:3838'}
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}
SERVICE = Service()
INSTOCK = False
MINUTE = 60  # sec
HOUR = 60 * 60  # min * sec
DAY = 24 * 60 * 60  # hours * min * sec

#code from https://zenscrape.com/how-to-build-a-simple-proxy-rotator-in-python/
def get_proxies():
    response = requests.get("https://sslproxies.org/")
    soup = BeautifulSoup(response.content, 'lxml')
    proxy = {'https': choice(list(map(lambda x:x[0]+':'+x[1], list(zip(map(lambda x:x.text, soup.findAll('td')[::8]), map(lambda x:x.text, soup.findAll('td')[1::8]))))))}
    return proxy


def get_request_result(url):
    while True:
        try:
            proxy = get_proxies()
            print("Proxy currently being used: {}".format(proxy))
            response = requests.get(url, proxies=proxy, timeout=7,headers=HEADERS)
            break
            # if the request is successful, no exception is raised
        except:
            print("Connection error, looking for another proxy")
            pass
    return response

def NewEgg():
    result = get_request_result('https://www.newegg.com/p/pl?d=rtx+3080')
    
    src = result.content
    print('status code', result.status_code)
    soup = BeautifulSoup(src,'lxml')
    
    products = []

    for div in soup.find_all('div',{'class':'item-container'}):
        a_tag = div.find('a')
        li_tag = div.find('li',{'class':'price-current'})

        link = a_tag.attrs['href'].split(' ')[0]
        card_name = div.find('a',{'class':'item-title'}).get_text()
        availability = div.find('p').get_text()
        price = li_tag.find('strong').get_text() if li_tag.find('strong') else "UnKnown"
        if availability != "OUT OF STOCK":
            INSTOCK = False

        products.append(
            {
                'link':link,
                'card_name':card_name,
                'availability':availability,
                'price':price,
                'vender':'NewEgg'
            })
    return products

def BestBuy():
    result = requests.get('https://www.bestbuy.com/')
    src = result.content
    soup = BeautifulSoup(src,'lxml')
    print(result.status_code)
    print(soup.text)

    product = []

    li_list = soup.find_all('li',{'class': "sku-item-list"})
    print(li_list)



def mail_list(shop_products):
    msg_list = []
    
    for product in shop_products:
        msg = format_message(product)
        msg_list.append(msg)
    
    message = '<h> RTX 3080 Availability/Prices </h>\n' + '\n'.join(msg_list) + "\n<strong>This is an automated email notification for RTX 3080 prices<strong>"

    email(SERVICE,message)

def get_user_time():
    # hour * min/h * sec/min
    hour_sec = time.localtime()[3] * 60 * 60
    min_sec = time.localtime()[4] * 60
    sec = time.localtime()[5]
    return hour_sec + min_sec + sec


def StartClock():
    global INSTOCK
    passed_time = 0
    # gets users current time and adds it to the day passed
    day_passed = get_user_time()
    # checks at 1 p.m
    time_offset = HOUR * 13
    # pads time IF the program was started slightly before the passing time
    day_passed += DAY if day_passed < time_offset else 0
    # day_passed = 133140
     
    emailed_today = False

    while True:
        time.sleep(1)
        passed_time += 1
        day_passed += 1

        if passed_time >= MINUTE * 45:
            passed_time = 0
            if not emailed_today:
                products = NewEgg()

            if INSTOCK and not emailed_today:
                emailed_today = True
                print('Email sent!')
                mail_list(products)

            elif day_passed >= (DAY + time_offset) and not emailed_today and not INSTOCK:
                day_passed = get_user_time()
                print('Email sent!')
                mail_list(products)

            elif day_passed >= (DAY + time_offset) and emailed_today:
                print('Email has already been sent today! Reseting Timer')
                day_passed = get_user_time()
                emailed_today = False
                INSTOCK = False
        
        print('passed_time',passed_time,'day_passed',day_passed,'emailed_today',emailed_today,'time_threshold',(DAY + time_offset))
                 
    
if __name__ == '__main__':
    StartClock()
    # print(NewEgg())
    # r = requests.get('https://httpbin.org/ip',proxies=PROXIES)
    # print(r.text)
    # s = time.localtime()
    # print(s)
    # print('hour',s[4],'seconds',get_user_time())
