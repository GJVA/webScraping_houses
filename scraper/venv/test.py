import scrapy
import pymysql
import pandas as pd
import re
from time import sleep

connection = pymysql.connect("localhost", "root", "Greenpeace", "immo_scraper")

list_values = []
column_names = []
df_append = pd.DataFrame()

# from itertools import chain
# import os
#
# all_links = []
# alist = os.popen("scrapy runspider pages.py").read()
# splitted_list = alist.split()
# for link in splitted_list:
#     print(link.split("'")[1::2][0])
#     all_links.append(link.split("'")[1::2][0])
# print(all_links)

class BrickSetSpider(scrapy.Spider):
    name = "brickset_spider"
    start_urls = [
        #link for link in all_links
        #'https://www.zimmo.be/nl/leuven-3000/te-huur/appartement/JDN36/?search=b88703fc7ff9fe9bb41300cbc776e0c0'
        'https://www.zimmo.be/nl/leuven-3000/te-koop/appartement/HVLC2/?search=e94a0e220db4cf23fa1df88461dcbd16&boosted=1'
                  ]

    def start_request(self, parse):
        for url in self.start_urls:
            yield scrapy.Request(url)

    def parse(self, response):
        sleep(20)
        list_values = []
        column_names = []
        df_append = pd.DataFrame()

        column_names.append('Type')
        value = re.search('appartement|garage|huis|bedrijfsvastgoed|kot-kamer', response.request.url)
        list_values.append(value.group(0))

        ### Status van contract_Type
        column_names.append('Contract_Type')
        for brickset in response.xpath('//h1[contains(@class, "pand-title")]/text()'):
            print(brickset, '1')
            value = re.search('huur|koop', brickset.get())
            print(value, '2')
            if brickset.get() is None:
                list_values.append('NVT')
                print(brickset.css('h1::text').get(), '3')
            else:
                print(value.group(0), '4')
                list_values.append(value.group(0))
            break # make sure you only take the first one (stop iteration after the title)

        ### Address
        ADRESS_SELECTOR = '.section-title'
        print(response.css(ADRESS_SELECTOR).css('h2').css('span::text')[0].get())
        column_names.append('Adres')
        list_values.append(response.css(ADRESS_SELECTOR).css('h2').css('span::text')[0].get())

        ### Mobiscore
        MOBI_SELECTOR = '.section-mobiscore_score-wrapper'
        print(response.css(MOBI_SELECTOR).css('span').css('span::text')[0].get())
        column_names.append('Mobiscore')
        list_values.append(response.css(MOBI_SELECTOR).css('span').css('span::text')[0].get())

        ### Detail Information
        # Financieel
        for brickset in response.xpath('//div[contains(@class, "col-xsm-4 info-name")]/text()'):
            name = re.sub('[\W,.?!:\'\t\n ]+', '_', brickset.get())
            print(name)
            column_names.append(name)
        for brickset in response.xpath('//div[contains(@class, "col-xsm-8 info-value")]'):
            if (isinstance(brickset.css('div::text').get(), str)):
                value = re.search('(\d+(\.\d+)?)', brickset.css('div::text').get())
                if brickset.css('div::text').get() == None:
                    list_values.append('NVT')
                elif value is not None:
                    print(value.group(0))
                    list_values.append(value.group(0))
                else:
                    list_values.append('NVT')
            else:
                list_values.append('NVT')
                continue
        # Indeling
        for brickset in response.xpath('//div[contains(@class, "col-xsm-8 col-sm-3 info-name")]/text()'):
            name = re.sub('[\W,.?!:\'\t\n ]+', '_', brickset.get())
            print(name)
            column_names.append(name)
        for brickset in response.xpath('//div[contains(@class, "col-xsm-4 col-sm-3 info-value")]'):
            if brickset.css('div::text').get() == None:
                list_values.append('NVT')
                print(brickset.css('div::text').get())
            else:
                #value = re.search('(\d+([\.\,]\d+)?)',brickset.get())
                print(brickset.css('div::text').get())
                #print(value.group(0))
                #list_values.append(value.group(0))
                list_values.append(brickset.css('div::text').get())
        # Bebouwing
        for brickset in response.xpath('//div[contains(@class, "col-xs-7 info-name")]/text()'):
            name = re.sub('[\W,.?!:\'\t\n ]+', '_', brickset.get())
            print(name)
            column_names.append(name)
        for brickset in response.xpath('//div[contains(@class, "col-xs-5 info-value")]'):
            if brickset.css('div::text').get() == None:
                list_values.append('NVT')
                print(brickset.css('div::text').get())
            else:
                print(brickset.css('div::text').get())
                value = re.search('(?:^|(?<=\s))(?:\w{1,12}|(\d+([\.\,]\d+)?)|-)(?:$|(?=\s))',brickset.get())
                if value is None:
                    if brickset.css('div').css('.show-on-print').get() is None:
                        print('is none')
                        list_values.append('NVT')
                    elif "✓" in brickset.css('div').css('.show-on-print').get():
                        print('✓')
                        list_values.append('Ja')
                    elif "✗" in brickset.css('div').css('.show-on-print').get():
                        print('✗')
                        list_values.append('Nee')
                    else:
                        print('something else')
                else:
                    print(value.group(0))
                    if value.group(0) == '-':
                        list_values.append('NVT')
                    else:
                        list_values.append(value.group(0))

        print(column_names)
        print(list_values)
        df_append = pd.DataFrame([list_values], columns=column_names)
        print(df_append)

        ######## Check whether columns names in table are the ones that are captured on the web page
        sql_table_column_check = """SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = 'zimmo_information'"""
        cursor = connection.cursor()
        cursor.execute(sql_table_column_check)

        ### Fetch the column names from the table
        metadata = cursor.fetchall()
        metadata_list = []
        for data in metadata:
            metadata_list.append(data[0])
        print(metadata_list)

        ### Check whether column names in table are the same as in web page
        difference = list(set(column_names) - set(metadata_list))
        if not difference:
            print('the same length')
            sql_insert_query = "INSERT INTO zimmo_information" + ' ( ' + ','.join(column_names) + ' ) ' + 'values ' + ' ( ' + ','.join(['"' + x + '"' for x in list_values]) + ' ) '
            print(sql_insert_query)
            cursor.execute(sql_insert_query)
            connection.commit()
        else:
            ### If not the same, alter the table and add the extra columns, afterwards insert the values
            print('not the same length: ' + str(difference))
            sql_alter_table = "ALTER TABLE zimmo_information ADD" + ' ( ' + ','.join([x + " TEXT(255)" for x in difference]) + ' ) '
            print(sql_alter_table)
            sql_insert_query = "INSERT INTO zimmo_information" + ' ( ' + ','.join(column_names) + ' ) ' + 'values ' + ' ( ' + ','.join(['"' + x + '"' for x in list_values]) + ' ) '
            print(sql_insert_query)
            cursor.execute(sql_alter_table)
            cursor.execute(sql_insert_query)
            connection.commit()

