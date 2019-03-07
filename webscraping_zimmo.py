#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 21:21:43 2019

@author: gertjan.vanlook
"""
# import the requests library to make the calls to the server of the webpages you want to crawl. 
import requests
session = requests.session()

session.proxies = {} # Is the following needed? Is here where one can put it's proxies? 


# ================look up to IP address used & usage of Socks =================
# #r = session.get('http://httpbin.org/ip')
# #print(r.text)
# 
# #session.proxies['http'] = 'socks5h://localhost:9050'
# #session.proxies['https'] = 'socks5h://localhost:9050'
# 
# #r = session.get('https://httpbin.org/user-agent')
# #print(r.text)
# =============================================================================

# The 'headers' attribute is used to let the browser think that you're a human user. Because some webpage do not allow crawlers 
headers = {}
headers['User-agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'

# Set out the different proxies you want to use. Note that we use the random library such that we can randomly pick one of the following proxies for each request we make.
all_proxies = [{'http': 'http://51.75.202.252:80/'}, {'https': 'https://51.75.109.90:3128/'}, {'http': 'http://91.134.221.168:80/'}]
import random
proxy = random.choice(all_proxies)
print(proxy)

# The first galary page is put into a variable
r = session.get('https://www.zimmo.be/nl/panden/?status=2&hash=b473b87fe42ec10407d13d7a754e2bc1&priceIncludeUnknown=1&priceChangedOnly=0&bedroomsIncludeUnknown=1&bathroomsIncludeUnknown=1&constructionIncludeUnknown=1&livingAreaIncludeUnknown=1&landAreaIncludeUnknown=1&commercialAreaIncludeUnknown=1&yearOfConstructionIncludeUnknown=1&epcIncludeUnknown=1&queryCondition=and&includeNoPhotos=1&includeNoAddress=1&onlyRecent=0&onlyRecentlyUpdated=0&isPlus=0&region=list&district=MzCgLjAEAA%253D%253D#gallery', proxies=proxy, headers=headers)
r.text

# import libraries
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from time import sleep

# =========If you want to use urllib instead of requests library===============
# #specify the main url where all houses are shown in unordered list (This will als become a for loop 
# #through all pages of these unordered list of houses)
# main_url = 'https://www.zimmo.be/nl/panden/?status=2&hash=b473b87fe42ec10407d13d7a754e2bc1&priceIncludeUnknown=1&priceChangedOnly=0&bedroomsIncludeUnknown=1&bathroomsIncludeUnknown=1&constructionIncludeUnknown=1&livingAreaIncludeUnknown=1&landAreaIncludeUnknown=1&commercialAreaIncludeUnknown=1&yearOfConstructionIncludeUnknown=1&epcIncludeUnknown=1&queryCondition=and&includeNoPhotos=1&includeNoAddress=1&onlyRecent=0&onlyRecentlyUpdated=0&isPlus=0&region=list&district=MzCgLjAEAA%253D%253D#gallery'
# request = Request(main_url, headers = {'User-Agent': 'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543a Safari/419.3'})
# main_page = urlopen(request).read()
# print(main_page)
# =============================================================================

# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(r.text, 'html.parser')
# get the index price
url_to_house = soup.find_all('a', attrs={'class':'property-item_link'})
print(url_to_house)

#Loop through all 'a' attributes with the class mentioned in url_to_house and get the href if it exists
urls_houses_galary_1 = [] 
for a_tag in url_to_house:
    if 'href' in a_tag.attrs:
        urls_houses_galary_1.append('https://www.zimmo.be' + a_tag['href'])
        print(urls_houses_galary_1)
        sleep(10)



# Create empty objects for the variables you like
#adres = []
prijs = [] 
gemeenschap_prijs = []
onroerend_voorheffing_prijs = []  
#soort_advertentie = []
#vastgoed_type = []
#aantal_kamers = []
#aantal_badkamers = []
#oppervlakte = []
#parking = []

#Get the variables VIA requests library
import re
for i in range(0, len(urls_houses_galary_1)):
   s = session.get(urls_houses_galary_1[i], proxies=proxy, headers= headers)
   #single_page_html =  s.text
   soup_single_page = BeautifulSoup(s.text[50000:60000], 'html.parser')
   sleep(20)
   try:
       div_attr_house_price = soup_single_page.find_all('div', attrs={'class':'col-xsm-8 info-value'})[0]
       price_val_change = re.search('(\d+(\.\d+)?)',div_attr_house_price.text)
       print(price_val_change.group(0))
       prijs.append(price_val_change.group(0))
       sleep(20) 
   except:
       print('NVT - prijs')
       prijs.append('NVT')
       sleep(20) 
   try:
       div_attr_house_gemeenschap_price = soup_single_page.find_all('div', attrs={'class':'col-xsm-8 info-value'})[1]
       gemeen_price_val_change = re.search('(\d+(\.\d+)?)',div_attr_house_gemeenschap_price.text)
       print(gemeen_price_val_change.group(0))
       gemeenschap_prijs.append(gemeen_price_val_change.group(0))
       sleep(20) 
   except:
       print('NVT - gemeenschaps. prijs')
       gemeenschap_prijs.append('NVT')
       sleep(20) 
   try:
       div_attr_house_gemeenschap_price = soup_single_page.find_all('div', attrs={'class':'col-xsm-8 info-value'})[2]
       onroer_price_val_change = re.search('(\d+(\.\d+)?)',div_attr_house_gemeenschap_price.text)
       print(onroer_price_val_change.group(0))
       onroerend_voorheffing_prijs.append(onroer_price_val_change.group(0))
       sleep(20) 
   except:
       print('NVT - onroer. voorhef. prijs')
       onroerend_voorheffing_prijs.append('NVT') 
       sleep(20) 
   sleep(20) 


# =============================================================================
# # Get the variables VIA urllib library
# import re
# for i in range(0, len(urls_houses_galary_1)):
#    request = Request(urls_houses_galary_1[i], headers = {'User-Agent' :\
#                                           "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36"})
#    single_page_html = urlopen(request).read()
#    print(single_page_html)
#    soup_single_page = BeautifulSoup(single_page_html, 'html.parser')
#    sleep(10)
#    try:
#        div_attr_house_price = soup_single_page.find_all('div', attrs={'class':'col-xsm-8 info-value'})[0]
#        price_val_change = re.search('€.(\d+(\.\d+)?)',div_attr_house_price.text)
#        print(price_val_change.group(0))
#        prijs.append(price_val_change.group(0))
#        sleep(10) 
#    except:
#        print('NVT - prijs')
#        prijs.append('NVT')
#        sleep(10) 
#    try:
#        div_attr_house_gemeenschap_price = soup_single_page.find_all('div', attrs={'class':'col-xsm-8 info-value'})[1]
#        gemeen_price_val_change = re.search('€.(\d+(\.\d+)?)',div_attr_house_gemeenschap_price.text)
#        print(gemeen_price_val_change.group(0))
#        gemeenschap_prijs.append(gemeen_price_val_change.group(0))
#        sleep(10) 
#    except:
#        print('NVT - gemeenschaps. prijs')
#        gemeenschap_prijs.append('NVT')
#        sleep(10) 
#    try:
#        div_attr_house_gemeenschap_price = soup_single_page.find_all('div', attrs={'class':'col-xsm-8 info-value'})[2]
#        onroer_price_val_change = re.search('€.(\d+(\.\d+)?)',div_attr_house_gemeenschap_price.text)
#        print(onroer_price_val_change.group(0))
#        onroerend_voorheffing_prijs.append(onroer_price_val_change.group(0))
#        sleep(10) 
#    except:
#        print('NVT - onroer. voorhef. prijs')
#        onroerend_voorheffing_prijs.append('NVT') 
#        sleep(10) 
#    sleep(10) 
# =============================================================================



### Create one tabel with data

import pandas as pd 
# Create a values as dictionary of lists
raw_data = {'prijs': prijs, 
        'gemeenschap_prijs': gemeenschap_prijs, 
        'onroerend_voorheffing_prijs': onroerend_voorheffing_prijs
        }

# Create a dataframe
df = pd.DataFrame(raw_data)

# View a dataframe
df

#----------------------------------------------------

##### Haal de andere galaries op om data van te halen 
urls_other_galaries = []
for i in range(2,14):
    new_galary_url = 'https://www.zimmo.be/nl/panden/?status=2&hash=c6bd583e0a1c97acb8314b6772d02ade&priceIncludeUnknown=1&priceChangedOnly=0&bedroomsIncludeUnknown=1&bathroomsIncludeUnknown=1&constructionIncludeUnknown=1&livingAreaIncludeUnknown=1&landAreaIncludeUnknown=1&commercialAreaIncludeUnknown=1&yearOfConstructionIncludeUnknown=1&epcIncludeUnknown=1&queryCondition=and&includeNoPhotos=1&includeNoAddress=1&onlyRecent=0&onlyRecentlyUpdated=0&isPlus=0&excludedEstates%5B0%5D=IHZHB&excludedEstates%5B1%5D=IJC2W&excludedEstates%5B2%5D=ILQFS&excludedEstates%5B3%5D=IOYWZ&region=list&district=MzCgLjAEAA%253D%253D&pagina=' + str(i)
    urls_other_galaries.append(new_galary_url)


# Get the subpages on the galaries
a_houses_other_galaries = []
for i in range(0,len(urls_other_galaries)):
    proxy = random.choice(all_proxies)
    print(proxy)
    r_other = session.get(urls_other_galaries[i], proxies=proxy, headers=headers)
    print(r_other.text)     
    soup_sub_galaries = BeautifulSoup(r_other.text, 'html.parser')
    # get the index price
    url_to_house_sub = soup_sub_galaries.find_all('a', attrs={'class':'property-item_link'})
    a_houses_other_galaries.append(url_to_house_sub)
    sleep(15)


#Loop through all 'a' attributes with the class mentioned in url_to_house and get the href if it exists
urls_houses_other_galaries = [] 
for i in range(0, len(a_houses_other_galaries)):
    for a_tag in a_houses_other_galaries[i]:
        if 'href' in a_tag.attrs:
            urls_houses_other_galaries.append('https://www.zimmo.be' + a_tag['href'])
            print(urls_houses_other_galaries)
            sleep(1)



#Get the variables VIA requests library
import re
for i in range(0, len(urls_houses_galary_1)):
   s = session.get(urls_houses_galary_1[i], proxies=proxy, headers= headers)
   #single_page_html =  s.text
   soup_single_page = BeautifulSoup(s.text[50000:60000], 'html.parser')
   sleep(20)

 # Get the variables (prices only)
import re
from requests.exceptions import ProxyError

for i in range(0, len(urls_houses_other_galaries)):
   try:
       proxy = random.choice(all_proxies)
       print(proxy)
       s = session.get(urls_houses_other_galaries[i], proxies=proxy, headers= headers)
       soup_single_page = BeautifulSoup(s.text[50000:60000], 'html.parser')
       sleep(10)
   except ProxyError:
       pass
   try:
       div_attr_house_price = soup_single_page.find_all('div', attrs={'class':'col-xsm-8 info-value'})[0]
       price_val_change = re.search('(\d+(\.\d+)?)',div_attr_house_price.text)
       print(price_val_change.group(0))
       prijs.append(price_val_change.group(0))
       sleep(10) 
   except:
       print('NVT - prijs')
       prijs.append('NVT')
       sleep(10) 
   try:
       div_attr_house_gemeenschap_price = soup_single_page.find_all('div', attrs={'class':'col-xsm-8 info-value'})[1]
       gemeen_price_val_change = re.search('(\d+(\.\d+)?)',div_attr_house_gemeenschap_price.text)
       print(gemeen_price_val_change.group(0))
       gemeenschap_prijs.append(gemeen_price_val_change.group(0))
       sleep(10) 
   except:
       print('NVT - gemeenschaps. prijs')
       gemeenschap_prijs.append('NVT')
       sleep(10) 
   try:
       div_attr_house_gemeenschap_price = soup_single_page.find_all('div', attrs={'class':'col-xsm-8 info-value'})[2]
       onroer_price_val_change = re.search('(\d+(\.\d+)?)',div_attr_house_gemeenschap_price.text)
       print(onroer_price_val_change.group(0))
       onroerend_voorheffing_prijs.append(onroer_price_val_change.group(0))
       sleep(10) 
   except:
       print('NVT - onroer. voorhef. prijs')
       onroerend_voorheffing_prijs.append('NVT') 
       sleep(10) 
   sleep(15) 
   



# =============================================================================
# ###############################################################################    
# # Try out to get other data from the webpage
# bouwjaar = []
# for i in range(0, len(urls_houses_other_galaries)):
#     try:
#         proxy = random.choice(all_proxies)
#         print(proxy)
#         s = session.get(urls_houses_other_galaries[i], proxies=proxy, headers= headers)
#         soup_single_page = BeautifulSoup(s.text[50000:60000], 'html.parser')
#     except ProxyError:
#         print('error de la proxy!')
#         pass
#     try:
#         div_attr_house_bouwjaar = soup_single_page.find_all('div', attrs={'class':'col-xs-5 info-value'})
#         bouwjaar_val_change = re.search('\d{4}',div_attr_house_bouwjaar.text)
#         print(bouwjaar_val_change.group(0))
#         bouwjaar.append(bouwjaar_val_change.group(0))
#         sleep(10) 
#     except:
#         print('NVT - bouwjaar')
#         prijs.append('NVT')
#         sleep(10)
#     sleep(15)
# =============================================================================

#--------------- Get the different types of variables and their values and add them ------#
#--------------- to the df2 dataframe ----------------------------------------------------#
   
import re
from requests.exceptions import ProxyError
import pandas as pd 
# Try out with one 
column_list = ['Prijs'
               ,'Aantal badkamers'
               ,'Aantal slaapkamers'
               ,"Aantal wc's"
               ,'Bebouwing'
               ,'Woonopp.'
               ,'EPC-waarde'
               ]
df2 = pd.DataFrame(columns = column_list)
df2

df_append = pd.DataFrame()
columns = []
list1 = []
div_attr_house_names = []

for i in range(0, len(urls_houses_galary_1)):
    try:
        proxy = random.choice(all_proxies)
        print(proxy)
        s = session.get(urls_houses_galary_1[i], proxies=proxy, headers= headers)
        soup_single_page = BeautifulSoup(s.text[30000:60000], 'html.parser')
    except ProxyError:
        print('error de la proxy!')
        soup_single_page.clear()
        pass
    try:
        print('GJ: nu halen we data op van webpage')
        adress_house_div = soup_single_page.find_all('div', attrs={'class':'section-title-block'})[0]
        adress_house_span = adress_house_div.find('span').text
        print(adress_house_span)
        div_attr_house_names = soup_single_page.find_all('div', attrs={'class':'col-xs-7 info-name'})
        div_attr_house_values = soup_single_page.find_all('div', attrs={'class':'col-xs-5 info-value'})
        print(div_attr_house_names)
        print(div_attr_house_values)
        sleep(10) 
    except:
        print('NVT - no values')
        sleep(10)
    sleep(15)
    print('GJ: nu beginnen we met de for loop voor omzetten van data naar juiste formaat') 
    columns.clear()
    list1.clear()
    df_append = pd.DataFrame()     
    try:
        columns.append('Adres')
        list1.append([adress_house_span])
    except:
        pass
        print('GJ: no adress given')
    if div_attr_house_names:
        try:
            for i in range(0, len(div_attr_house_names)):
                test_name = div_attr_house_names[i].text
                print(div_attr_house_names[i].text)
                test = re.search('(?:^|(?<=\s))(?:\w{1,12}|\d{1,5}|✓)(?:$|(?=\s))',div_attr_house_values[i].text)
                print(test)
                columns.append(test_name)
                list1.append([test.group(0)])
                print(columns)
                print(list1)
                df_append = pd.DataFrame([list1], columns=columns)  
            if df_append.empty:
                print('empty dataframe')
                del df_append
            else:
                print('add to dataframe') 
                df2 = df2.append(df_append, sort=True) 
                df2
                del df_append
                del test_name
                del test
                del adress_house_div
                del adress_house_span
                del div_attr_house_names
                del div_attr_house_values
        except:
            print('GJ: no div_attr_house_names available')
            pass
    

# =============================================================================
# #------ Manier van werken ---------
# df_test_1 = pd.DataFrame(columns = ['Bebouwing', 'Prijs', 'Bouwjaar'])
# kolommen = ['Bebouwing', 'Prijs', 'Bouwjaar']
# waarden = ['Gesloten', '500', '2012']
# waarden_2 = ['Gesloten', '233', '2019']
# df_test_2 = pd.DataFrame([waarden], columns = kolommen)
# df_test_3 = pd.DataFrame([waarden_2], columns = kolommen)
# df_test_1 = df_test_1.append(df_test_2, sort=True)
# df_test_1 = df_test_1.append(df_test_3, sort=True)
# =============================================================================
       
# Trying to schedule times to run script
import datetime, schedule, time

TIME = [('6.03.2019', '06:41:00', 'abc.php?xxx'),
    ('6.03.2019', '10:00:30', 'abc.php?yyy'),
    ('6.03.2019', '12:00:30', 'abc.php?zzz'),
    ('6.03.2019', '14:30:30', 'abc.php?www')]

def job():
    global TIME
    date = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    for i in TIME:
        runTime = i[0] + " " + i[1]
        if i and date == str(runTime):            
            for i in range(0, len(urls_houses_other_galaries)):
                try:
                    proxy = random.choice(all_proxies)
                    print(proxy)    
                    s = session.get(urls_houses_other_galaries[i], proxies=proxy, headers= headers)
                    soup_single_page = BeautifulSoup(s.text[30000:60000], 'html.parser')
                except ProxyError:
                    print('error de la proxy!')
                    soup_single_page.clear()
                    pass
                try:
                    print('GJ: nu halen we data op van webpage')
                    adress_house_div = soup_single_page.find_all('div', attrs={'class':'section-title-block'})[0]
                    adress_house_span = adress_house_div.find('span').text
                    print(adress_house_span)
                    div_attr_house_names = soup_single_page.find_all('div', attrs={'class':'col-xs-7 info-name'})
                    div_attr_house_values = soup_single_page.find_all('div', attrs={'class':'col-xs-5 info-value'})
                    print(div_attr_house_names)
                    print(div_attr_house_values)
        
                    div_attr_house_price_name = soup_single_page.find_all('div', attrs={'class':'col-xsm-4 info-name'})
                    div_attr_house_price = soup_single_page.find_all('div', attrs={'class':'col-xsm-8 info-value'})
                    print(div_attr_house_price_name)
                    print(div_attr_house_price)
        
                    sleep(10) 
                except:
                    print('NVT - no values')
                    sleep(10)
                sleep(15)
                columns.clear()
                list1.clear()
                df_append = pd.DataFrame()     
                try:
                    columns.append('Adres')
                    list1.append([adress_house_span])
                except:
                    pass
                    print('GJ: no adress given')
            
                print('GJ: nu beginnen we met de for loop voor omzetten van data naar juiste formaat') 
                if div_attr_house_names:
                    try:
                        if div_attr_house_price_name:
                            for i in range(0, len(div_attr_house_price_name)):    
                                allPrices = re.search('(\d+(\.\d+)?)',div_attr_house_price[i].text)
                                print(allPrices)
                                list1.append([allPrices.group(0)])
                                allPrices_name = div_attr_house_price_name[i].text
                                columns.append(allPrices_name)
                                print(allPrices_name)
                                sleep(10) 
                            else:
                                print('GJ: no prices available')
                        for i in range(0, len(div_attr_house_names)):
                            test_name = div_attr_house_names[i].text
                            print(div_attr_house_names[i].text)
                            test = re.search('(?:^|(?<=\s))(?:\w{1,12}|\d{1,5}|✓)(?:$|(?=\s))',div_attr_house_values[i].text)
                            print(test)
                            columns.append(test_name)
                            list1.append([test.group(0)])
                            print(columns)
                            print(list1)
                            df_append = pd.DataFrame([list1], columns=columns)
            
                        if df_append.empty:
                            print('empty dataframe')
                            del df_append
                        else:
                            print('add to dataframe') 
                            df2 = df2.append(df_append, sort=True) 
                            df2
                            del df_append
                            del test_name
                            del test
                
                            del allPrices
                            del allPrices_name
                            del allPrices
                            del allPrices_name
                
                            del adress_house_div
                            del adress_house_span
                            del div_attr_house_names
                            del div_attr_house_values
                    except:
                        print('GJ: no div_attr_house_names available')
                        pass
    
#schedule.every(0.10).minutes.do(job)
schedule.every(1).hours.do(job)
while True:
    schedule.run_pending()
    time.sleep(1)
        


## TRYYY OUT WITH PRICES
            
import re
from requests.exceptions import ProxyError
import pandas as pd 
# Try out with one 
column_list = ['Prijs'
               ,'Aantal badkamers'
               ,'Aantal slaapkamers'
               ,"Aantal wc's"
               ,'Bebouwing'
               ,'Woonopp.'
               ,'EPC-waarde'
               ]
df2 = pd.DataFrame(columns = column_list)
df2

df_append = pd.DataFrame()
columns = []
list1 = []

for i in range(0, len(urls_houses_other_galaries)):
    columns.clear()
    list1.clear()
    #df_append = pd.DataFrame()
    try:
        proxy = random.choice(all_proxies)
        print(proxy)
        s = session.get(urls_houses_other_galaries[i], proxies=proxy, headers= headers)
        soup_single_page = BeautifulSoup(s.text[30000:60000], 'html.parser')
    except ProxyError:
        print('error de la proxy!')
        soup_single_page.clear()
        pass
   # except requests.exceptions.Timeout:
    # Maybe set up for a retry, or continue in a retry loop
      # print('timeout')
       # pass
    #except requests.exceptions.TooManyRedirects:
    # Tell the user their URL was bad and try a different one
      #  print('toomanyredirects')
      #  pass
    except requests.exceptions.RequestException as e:
    # catastrophic error. bail.
        print(e)
        pass
    try:
        print('GJ: nu halen we data op van webpage')
        adress_house_div = soup_single_page.find_all('div', attrs={'class':'section-title-block'})[0]
        adress_house_span = adress_house_div.find('span').text
        print(adress_house_span)
        div_attr_house_names = soup_single_page.find_all('div', attrs={'class':'col-xs-7 info-name'})
        div_attr_house_values = soup_single_page.find_all('div', attrs={'class':'col-xs-5 info-value'})
        print(div_attr_house_names)
        print(div_attr_house_values)
        
        div_attr_house_price_name = soup_single_page.find_all('div', attrs={'class':'col-xsm-4 info-name'})
        div_attr_house_price = soup_single_page.find_all('div', attrs={'class':'col-xsm-8 info-value'})
        print(div_attr_house_price_name)
        print(div_attr_house_price)
        
        sleep(10) 
    except:
        print('NVT - no values')
        sleep(10)
        pass
    sleep(15)   
    try:
        columns.append('Adres')
        list1.append([adress_house_span])
    except:
        pass
        print('GJ: no adress given')
            
    print('GJ: nu beginnen we met de for loop voor omzetten van data naar juiste formaat') 
    if div_attr_house_names:
        try:
            if div_attr_house_price_name:
                for i in range(0, len(div_attr_house_price_name)):    
                    allPrices = re.search('(\d+(\.\d+)?)',div_attr_house_price[i].text)
                    print(allPrices)
                    list1.append([allPrices.group(0)])
                    allPrices_name = div_attr_house_price_name[i].text
                    columns.append(allPrices_name)
                    print(allPrices_name)
                    sleep(10) 
                else:
                    print('GJ: no prices available')
            for i in range(0, len(div_attr_house_names)):
                test_name = div_attr_house_names[i].text
                print(div_attr_house_names[i].text)
                test = re.search('(?:^|(?<=\s))(?:\w{1,12}|\d{1,5}|✓)(?:$|(?=\s))',div_attr_house_values[i].text)
                print(test)
                columns.append(test_name)
                list1.append([test.group(0)])
                print(columns)
                print(list1)
                df_append = pd.DataFrame([list1], columns=columns)
            
            df2 = df2.append(df_append, sort=True) 
            df2
            del df_append
            del test_name
            del test
            
            del allPrices
            del allPrices_name
            del allPrices
            del allPrices_name
            
            del adress_house_div
            del adress_house_span
            del div_attr_house_names
            del div_attr_house_values 
            if df_append.empty:
                print('empty dataframe')
                del df_append
            else:
                print('add to dataframe') 
                df2 = df2.append(df_append, sort=True) 
                df2
                del df_append
                del test_name
                del test
                
                del allPrices
                del allPrices_name
                del allPrices
                del allPrices_name
                
                del adress_house_div
                del adress_house_span
                del div_attr_house_names
                del div_attr_house_values
        except:
            print('GJ: no div_attr_house_names available')
            pass
    
       







