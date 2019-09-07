from itertools import chain
import os

all_links = []
alist = os.popen("scrapy runspider pages.py").read()
splitted_list = alist.split()
for link in splitted_list:
    print(link.split("'")[1::2][0])
    all_links.append(link.split("'")[1::2][0])
print(all_links)