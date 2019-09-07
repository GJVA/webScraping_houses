import scrapy
import re

all_href = []
all_links = []
class GetPages(scrapy.Spider):
    name = "Pages_spider"
    start_urls = [
        'https://www.zimmo.be/nl/panden/?status=2&hash=a44f7a59e05d525fb5d376b2bbfe4d09&priceIncludeUnknown=1&priceChangedOnly=0&bedroomsIncludeUnknown=1&bathroomsIncludeUnknown=1&constructionIncludeUnknown=1&livingAreaIncludeUnknown=1&landAreaIncludeUnknown=1&commercialAreaIncludeUnknown=1&yearOfConstructionIncludeUnknown=1&epcIncludeUnknown=1&queryCondition=and&includeNoPhotos=1&includeNoAddress=1&onlyRecent=0&onlyRecentlyUpdated=0&isPlus=0&region=list&city=MzAYicAQAA%253D%253D#gallery'
                  ]

    def parse(self, response):
        for href in response.css('ul.pagination a::attr(href)'):
            url = response.urljoin(href.extract())
            all_href.append(url)
            #print(url, 'begin')
        for i in range(2, int(all_href[-2].split('=')[-1])):
            yield scrapy.Request(all_href[1][:-1] + str(i), self.parse_follow)

    def parse_follow(self, response):
        for href in response.css('div.property-item a::attr(href)').extract():
            if 'javascript:void(0)' not in href:
                if 'https://www.zimmo.be' + href in all_links:
                    continue
                else:
                    all_links.append('https://www.zimmo.be' + href)
            else:
                continue
        print(all_links)
