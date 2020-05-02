import scrapy

class AustmpsItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    district = scrapy.Field()
    link = scrapy.Field()
    twitter = scrapy.Field()
    party = scrapy.Field()
    phonenumber = scrapy.Field()
    
class AustmpdataSpider(scrapy.Spider):
    name = 'austmpdata'  # The name of this spider
    
    # The allowed domain and the URLs where the spider should start crawling:
    allowed_domains = ['www.aph.gov.au']
    start_urls = ['http://www.aph.gov.au/Senators_and_Members/Parliamentarian_Search_Results?q=&mem=1&par=-1&gen=0&ps=0/']
    
    def parse(self, response):
        # The main method of the spider. It scrapes the URL(s) specified in the
        # 'start_url' argument above. The content of the scraped URL is passed on
        # as the 'response' object.

        # the function is an iterator, so we need to iterate over it. There is likely a cleaner way to do this.
        for item in self.scrape(response):
            yield item

    def scrape(self, response):
        for resource in response.xpath("//h4[@class='title']/.."):
            # Loop over each item on the page. 
            item = AustmpsItem() # Creating a new Item object

            item['name'] = resource.xpath("h4/a/text()").extract_first()
            item['link'] = resource.xpath("h4/a/@href").extract_first()
            item['district'] = resource.xpath("dl/dd/text()").extract_first()
            item['twitter'] = resource.xpath("dl/dd/a[contains(@class, 'twitter')]/@href").extract_first()
            item['party'] = resource.xpath("dl/dt[text()='Party']/following-sibling::dd/text()").extract_first()

            yield item