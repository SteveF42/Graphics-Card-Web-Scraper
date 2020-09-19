import requests
import pprint
from bs4 import BeautifulSoup
from SendEmail import format_message
from SendEmail import email
from GmailAPI import Service
import time


SERVICE = Service()
INSTOCK = False
MINUTE = 60
HOUR = MINUTE * 60
DAY = HOUR * 24


def NewEgg():
    result = requests.get('https://www.newegg.com/p/pl?d=rtx+3080')
    src = result.content
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
    pass

def mail_list():
    newEgg_products = NewEgg()
    msg_list = []
    for product in newEgg_products:
        msg = format_message(product)
        msg_list.append(msg)
    
    message = '<h> RTX 3080 Availability/Prices </h>\n' + '\n'.join(msg_list) + "\n<strong>This is an automated email notification for RTX 3080 prices<strong>"

    email(SERVICE,message)

def StartClock():
    global INSTOCK
    passed_time = 0
    #starts the timer at 1 p.m
    day_offset = HOUR * 13
    day_passed = HOUR + day_offset
    emailed_today = False

    while True:
        time.sleep(1)
        passed_time += 1
        day_passed += 1
        products = NewEgg()

        if passed_time >= MINUTE:
            passed_time = 0
            if INSTOCK and not emailed_today:
                emailed_today = True
                print('Email sent!')
            elif day_passed >= (DAY+day_offset) and not emailed_today and not INSTOCK:
                day_passed = 0
                print('Email sent!')
            elif day_passed >= (DAY + day_offset) and emailed_today:
                print('Email has already been sent today! Reseting Timer')
                emailed_today = False
                INSTOCK = False
                day_passed = 0
        
        print('passed_time',passed_time,'day_passed',day_passed,'emailed_today',emailed_today)
                 
    
if __name__ == '__main__':
    # StartClock()
    s = time.localtime()
    print(s[3])
