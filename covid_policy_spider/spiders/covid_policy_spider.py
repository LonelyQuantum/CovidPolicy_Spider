# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from bs4 import BeautifulSoup
import bs4

import pandas as pd

from urllib import parse

import math
import re
import os

from covid_policy_spider.items import AnnouncementItem



def remove_unchinese(s):
    pattern = re.compile(r'[^\u4e00-\u9fa5]')
    chinese = re.sub(pattern, '', str(s))
    return chinese

class AnnouncementSpider(scrapy.spiders.CrawlSpider):
    name = "announcement_spider"

    
    def __init__(self, city='广州', max_page=300):
        self.MAX_PAGE = max_page
        #Delete the previous version of the result
        if city + '.json' in os.listdir('results/json/'):
            os.remove('results/json/' + city + '.json')
        #Load the starting url and encoding for the city's government website
        websiteInfo = pd.read_csv('settings/city_govs.csv', index_col='city')
        self.start_urls = [websiteInfo['url'][city]]
        self.MAIN_PAGE_ENCODING = websiteInfo['main_page_encoding'][city]
        self.SUB_PAGE_ENCODING = websiteInfo['sub_page_encoding'][city]
        #Load the selectors for the city
        selectorInfo = pd.read_csv('settings/selector_settings.csv',index_col = 'city')
        self.NEWS_SELECTOR = selectorInfo['news_selector'][city]
        self.URL_SELECTOR = selectorInfo['url_selector'][city]
        self.NEXT_PAGE_SELECTOR = selectorInfo['next_page_selector'][city]
        self.TITLE_SELECTOR = selectorInfo['title_selector'][city]
        self.DATE_SELECTOR = selectorInfo['date_selector'][city]
        self.SOURCE_SELECTOR = selectorInfo['source_selector'][city]
        self.DPRT_SELECTOR = selectorInfo['department_selector'][city]
        self.CONTENT_SELECTOR = selectorInfo['content_selector'][city]
        self.counter = 0

        self.kwlist1 = ['暂停省际交通','封城','必须开放场所','中考延期','非社区常住居民','封闭式管理','非必须公共场所',
                       '聚集性办公场所','实名制登记','公共室外活动场所','业务暂停办理','开关门时间','境外回国人员',
                       '二级响应','全面禁止市场销售活禽','健康码','对外来车辆进行登记','禁止堂食','居民日常行动',
                       '一级响应','政府接管','紧急征用','防疫物资','外来人口','返校','隔离14天','流行病学',
                       '航班数量','社区排查','公共室内活动场所','非必要医疗服务','限量购买','大型公共聚集活动',
                       '扫码登记','定点医院','和临时隔离区','关闭不生产防疫物资的工厂','疫情防控期间临时政策','关闭学校和各类培训机构',
                       '限制每家每户前往超市的频率和人数','禁止携带、输送、交易与食用野生动物','暂停办理签证业务','关闭公共室内活动场所',
                       '暂停部分公交线路','关闭部分地铁出入口','防控'] 
        
        self.kwlist2 = ['冠状病毒','肺炎','新冠','疫情']
        
        page.select_one(self.NEXT_PAGE_SELECTOR)
    
    def parse(self, response):
        self.counter += 1
        options = webdriver.ChromeOptions()
        options.add_argument('headless')

        driver = webdriver.Chrome(options=options)
        driver.get(self.start_urls)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        #soup = BeautifulSoup(response.body.decode(self.MAIN_PAGE_ENCODING,'ignore'), 'html.parser')
        for news in soup.select(self.NEWS_SELECTOR):
            url = news['href']
            url = parse.urljoin(self.start_urls[0],url)
            if url is not None:
                yield response.follow(url,callback=self.parse_page)
        next_page = soup.select_one(self.NEXT_PAGE_SELECTOR)
        
        if next_page is not None and self.counter < self.MAX_PAGE:
            next_page_url = next_page['href']
            next_page_url = parse.urljoin(self.start_urls[0],next_page_url)

            yield response.follow(next_page_url, callback=self.parse)
    
    def parse_page(self, response):
        soup = BeautifulSoup(response.body.decode(self.SUB_PAGE_ENCODING,'ignore'),'html.parser')
        #Select target elements
        title = self.robust_select(soup, self.TITLE_SELECTOR)
        url = response.url
        date = self.robust_select(soup, self.DATE_SELECTOR)
        source = self.robust_select(soup, self.SOURCE_SELECTOR)
        department = self.robust_select(soup, self.DPRT_SELECTOR)
        content = self.robust_select(soup, self.CONTENT_SELECTOR)
        #Check target elements
        if self.page_qualify(title, source, date, department, content):
            yield AnnouncementItem(title=title, url=url, date=date, source=source)
    
    def page_qualify(self,title, source, date, department, content):
        return self.page_qualify_kw(content)
        return res
    
    def page_qualify_kw(self,content):
        return any(kw in content for kw in self.kwlist1) and any(kw in content for kw in self.kwlist2)
    
    def robust_select(self,soup,SELECTOR):
        if type(SELECTOR) is not str:
            return None
        else:
            res = soup.select(SELECTOR)
            if res is None:
                return None
            else:
                if len(res) == 1:
                    return res[0].text
                else:
                    rescombined = ''
                    for part in res:
                        rescombined += part.text
                    return rescombined
    
    def return_page(self,response):
        PAGE_SELECTOR = 'a.current::text'
        yield {'page':response.css(PAGE_SELECTOR).get()}
