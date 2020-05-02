import scrapy
from scrapy.http import Request
from bs4 import BeautifulSoup
import bs4

import re
import os

from covid_policy_spider.items import AnnouncementItem

if "results/json/广州.json" in os.listdir('./'):
        os.remove('results/json/广州.json')

def remove_unchinese(s):
    pattern = re.compile(r'[^\u4e00-\u9fa5]')
    chinese = re.sub(pattern, '', str(s))
    return chinese

class AnnouncementSpiderArchieve(scrapy.spiders.CrawlSpider):
    name = "announcement_spider_archive"
    start_urls = ['http://www.gz.gov.cn/xw/tzgg/']
    
    def __init__(self, city='广州'):
        self.source_wanted = ['广州市防控新型冠状病毒肺炎疫情工作指挥部办公室','广州市防控新型冠状病毒肺炎疫情']
        self.source_test = ['广州市商务局']
        self.source_try = ['广州市防控新型冠状病毒肺炎疫情工作指挥部办公室', '广州市人民政府办公厅',
                           '广州市防控新型冠状病毒感染的肺炎疫情工作指挥部办公室', 
                  '市政府办公厅', '广州市卫生健康委员会','广州市防控新型冠状病毒感染的肺炎疫情工作指挥部']
        self.source_intended = self.source_try
        self.source_contained = '广州市防控'

        self.kwlist = ['暂停省际交通','封城','必须开放场所','中考延期','非社区常住居民','封闭式管理','非必须公共场所',
                       '聚集性办公场所','实名制登记','公共室外活动场所','业务暂停办理','开关门时间','境外回国人员',
                       '二级响应','全面禁止市场销售活禽','健康码','对外来车辆进行登记','禁止堂食','居民日常行动',
                       '一级响应','政府接管','紧急征用','防疫物资','外来人口','返校','隔离14天','流行病学',
                       '航班数量','社区排查','公共室内活动场所','非必要医疗服务','限量购买','大型公共聚集活动',
                       '扫码登记','定点医院','和临时隔离区','关闭不生产防疫物资的工厂','疫情防控期间临时政策','关闭学校和各类培训机构',
                       '限制每家每户前往超市的频率和人数','禁止携带、输送、交易与食用野生动物','暂停办理签证业务','关闭公共室内活动场所',
                       '暂停部分公交线路','关闭部分地铁出入口','防控'] 
        
        self.mainkws = ['冠状病毒','肺炎','新冠','疫情']
    
    def parse(self, response):
        NEWS_SELECTOR = 'ul.news_list>li'
        for news in response.css(NEWS_SELECTOR):
            URL_SELECTOR = 'a::attr(href)'
            url = news.css(URL_SELECTOR).get()
            if url is not None:
                yield response.follow(url,callback=self.parse_page)
        NEXT_PAGE_SELECTOR = 'a.next::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
    
    def parse_page(self, response):
        soup = BeautifulSoup(response.text,'html.parser')
        TITLE_SELECTOR = 'h1.content_title'
        DATE_SELECTOR = 'ul.fl > li.date > span'
        SOURCE_SELECTOR = '#laiyuan > b'
        DPRT_SELECTOR = '#zoomcon > p[style="text\-align\: right\;"]'
        CONTENT_SELECTOR = '#zoomcon > p'
        title = soup.select_one(TITLE_SELECTOR).text
        url = response.url
        date = soup.select_one(DATE_SELECTOR).text
        source = soup.select_one(SOURCE_SELECTOR).text
        department_raw = soup.select(DPRT_SELECTOR)
        department = ''
        if type(department_raw) == bs4.element.ResultSet:
            for part in department_raw:
                department += part.text
        else: 
            department = department_raw.text
        content_raw = soup.select(CONTENT_SELECTOR)
        content = ''
        if type(content_raw) == bs4.element.ResultSet:
            for part in content_raw:
                content += part.text
        else: 
            content = content.text
        if self.page_qualify(title, source, date, department, content):
            yield AnnouncementItem(title=title, url=url, date=date, source=source)
    
    def page_qualify(self,title, source, date, department, content):
        return self.page_qualify_kw(content)
        res = False
        res = res or department in self.source_intended or source in self.source_intended
        res = res or self.source_contained in department
        res = res or any(kw in content for kw in self.kwlist)
        return res
    
    def page_qualify_kw(self,content):
        return any(kw in content for kw in self.kwlist) and any(kw in content for kw in self.mainkws)
    
    def return_page(self,response):
        PAGE_SELECTOR = 'a.current::text'
        yield {'page':response.css(PAGE_SELECTOR).get()}