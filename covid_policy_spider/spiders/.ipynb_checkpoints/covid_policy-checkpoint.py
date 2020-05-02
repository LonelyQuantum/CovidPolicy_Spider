# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.3.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import scrapy


class AnnouncementSpider(scrapy.Spider):
    name = "announcement_spider"
    start_urls = ['http://www.gz.gov.cn/xw/tzgg/']
    
    def parse(self, response):
        NEWS_SELECTOR = 'ul.newslist>li'
        for newslist in response.css(NEWS_SELECTOR):
            
            TITLE_SELECTOR = 'a::text'
            yield {
                'name': newslist.css(TITLE_SELECTOR).extract_first(),
            }



