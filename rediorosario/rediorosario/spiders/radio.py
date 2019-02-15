# -*- coding: utf-8 -*-
import scrapy
import requests
import os
from urllib.parse import unquote

class RadioSpider(scrapy.Spider):

    name = 'radio'
    #allowed_domains = ['http://www.net11.com.br/radiorosario/']
    start_urls = ['http://www.net11.com.br/radiorosario//']
    file_extensions = ['.mb','.sfap0','.aif', '.cda', '.mid', '.midi', '.mp3', '.mpa', '.ogg', '.wav', '.wma', '.wpl', '.7z', '.arj', '.deb', '.pkg', '.rar', '.rpm', '.tar.gz', '.z', '.zip', '.bin', '.dmg', '.iso', '.toast', '.vcd', '.csv', '.dat', '.db', '.dbf', '.log', '.mdb', '.sav', '.sql', '.tar', '.xml', '.apk', '.bat', '.bin', '.cgi', '.pl', '.com', '.exe', '.gadget', '.jar', '.py', '.wsf', '.fnt', '.fon', '.otf', '.ttf', '.ai', '.bmp', '.gif', '.ico', '.jpeg', '.jpg', '.png', '.ps', '.psd', '.svg', '.tif', '.tiff', '.asp', '.aspx', '.cer', '.cfm', '.cgi', '.pl', '.css', '.htm', '.html', '.js', '.jsp', '.part', '.php', '.py', '.rss', '.xhtml', '.key', '.odp', '.pps', '.ppt', '.pptx', '.c', '.class', '.cpp', '.cs', '.h', '.java', '.sh', '.swift', '.vb', '.ods', '.xlr', '.xls', '.xlsx', '.bak', '.cab', '.cfg', '.cpl', '.cur', '.dll', '.dmp', '.drv', '.icns', '.ico', '.ini', '.lnk', '.msi', '.sys', '.tmp', '.3g2', '.3gp', '.avi', '.flv', '.h264', '.m4v', '.mkv', '.mov', '.mp4', '.mpg', '.mpeg', '.rm', '.swf', '.vob', '.wmv', '.doc', '.docx', '.odt', '.pdf', '.rtf', '.tex', '.txt', '.wks', '.wps', '.wpd']
    def parse(self, response):
        item_links = response.css("tr td a")
        #print (item_links)
        if item_links is not None:
        
            for item_link in item_links:
                url = item_link.css('a::attr(href)').extract_first()
                name = item_link.css('a::text').extract_first()
                next_page = response.urljoin(url)

                if self.check_is_file(url):
                    folder_path = unquote(response.url[37:])
                    file_path = os.path.join(folder_path,name)
                    #self.download_file(folder_path,file_path,next_page, name)
                    yield {'url':next_page,'folder':folder_path,'file_path':file_path,'name':name}
                else:
                    yield scrapy.Request(next_page, callback=self.parse)

    def check_is_file(self,url):
        if '.' in url:
            file_extension = '.' + url.split('.')[-1].lower()
            return file_extension in self.file_extensions
        return False


    def download_file(self,folder_path,file_path,url,name_file):

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        if not os.path.exists(file_path):
            r = requests.get(url) 
            with open(file_path,'wb') as f:
                f.write(r.content)
                r.close()
        
        