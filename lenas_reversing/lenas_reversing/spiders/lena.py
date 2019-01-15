# -*- coding: utf-8 -*-
import scrapy
import requests
import os
class LenaSpider(scrapy.Spider):
    folder_path = '/home/sec/rs/lena'
    name = 'lena'
    #allowed_domains = ['https://tuts4you.com/download/category/17//']
    start_urls = ['https://tuts4you.com/download/category/17//?order=name&sort=desc&view=50']

    def parse(self, response):
        rows = response.css("#download tr")
        for row in rows[1:-2]:
            name = row.css('td')[0].css('a::text').extract_first()
            url = row.css('td')[-1].css('a::attr(href)').extract_first()
            if (name and url):
                url = response.urljoin(url)
                
                r = requests.get(url)
                with open(os.path.join(self.folder_path,name),'wb') as f:
                    f.write(r.content)
            yield {'name':name,'url':url}
        
