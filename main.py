import requests
import pprint
from bs4 import BeautifulSoup
from SendEmail import format_message
from SendEmail import email
from GmailAPI import Service


SERVICE = Service()
INSTOCK = False

def NewEgg():
    result = requests.get('https://www.newegg.com/p/pl?d=rtx+3080')
    print("Status Code:", result.status_code)
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


def StartClock():
    pass

if __name__ == '__main__':
    newEgg_products = NewEgg()
    msg_list = []
    for product in newEgg_products:
        msg = format_message(product)
        msg_list.append(msg)
    
    message = '<h> RTX 3080 Availability/Prices </h>\n' + '\n'.join(msg_list) + "\n<strong>This is an automated email notification for RTX 3080 prices<strong>"

    email(SERVICE,message)
