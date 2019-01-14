# -*- coding: utf-8 -*-
import scrapy
import os
from scrapy.http import Request
import copy
from ..items import BookItem

class BookSpider(scrapy.Spider):
    name = 'book'
    #allowed_domains = ['http://index-of.es/']
    start_urls = ['http://index-of.es//']

    def parse(self, response):
        item_links = response.css(".buybox-content pre a")

        if item_links is not None:
        
            for item_link in item_links:
        
                if len(item_link.css("img").extract()) == 0:
        
                    url = item_link.css('a::attr(href)').extract_first()
                    name = item_link.css('a::text').extract_first()
        
                    if name != "Name" and name != "Size":
                        if not url.endswith('/'):
                            path = name
                            if response.meta and response.meta.get('path'):
                                path = os.path.join(response.meta["path"], name)
                            yield BookItem(name=name,path=path,url=response.urljoin(url)) 
                        else:
                            if response.meta and response.meta.get('path'):
                                meta = copy.deepcopy(response.meta)
                                meta["path"] = os.path.join(meta["path"], name)
                            else:
                                meta = {"path": name}
                            next_page = response.urljoin(url)
                            yield scrapy.Request(next_page, callback=self.parse, meta=meta)
