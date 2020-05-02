import scrapy
from scrapy.http import Request
from bs4 import BeautifulSoup
import bs4

class Gov_Announcement_Spider(scrapy.spiders.CrawlSpider):
    name = "gov_spider"
    baseurl = 'https://www.baidu.com/s?&wd='
    cities = ['广州', '北京', '上海', '深圳', '哈尔滨', '南宁', '太原', '长春', '合肥', '南昌', '重庆', '天津', 
              '海口', '贵阳', '石家庄', '成都', '杭州', '武汉', '南京', '长沙', '郑州', '青岛', '沈阳', '福州', 
              '昆明']
    start_urls = []
    for city in start_urls:
        start_urls.append(baseurl+city)
        
    def parse(self, response):
        FIRST_RESULT_SELECTOR = '#\31  > h3'
        for news in response.css(NEWS_SELECTOR):
            URL_SELECTOR = 'a::attr(href)'
            url = news.css(URL_SELECTOR).get()
            if url is not None:
                yield response.follow(url,callback=self.parse_page)
        NEXT_PAGE_SELECTOR = 'a.next::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
    
    