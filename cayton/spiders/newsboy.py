import scrapy
import pandas as pd
import datetime
from cayton.items import CaytonItem

first = 'https://chroniclingamerica.loc.gov/lccn/sn87093353/'
last = '/ed-1/'
ocr = 'ocr/'

start = datetime.date(1917,7,14)
end = datetime.date(1921,2,1)

saturdays = pd.date_range(start=start, end=end, freq='W-SAT')

urls = []

for n in saturdays:
    url = first + str(n.year) + '-' + str(n.month).zfill(2) + '-' + str(n.day).zfill(2) + last
    urls.append(url)

class NewsboySpider(scrapy.spiders.CrawlSpider):
    name = 'newsboy'
    allowed_domains = ['chroniclingamerica.loc.gov']
    start_urls = urls
    le1 = scrapy.linkextractors.LinkExtractor(allow=r'seq-\d/$')
    le2 = scrapy.linkextractors.LinkExtractor(allow=r'ocr/')
    
    rules = [
        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        scrapy.spiders.Rule(le1),
        scrapy.spiders.Rule(le2, callback='parse_page')]


    def parse_page(self, response):
    	item = CaytonItem()
    	item['url'] = response.url
    	item['text'] = response.xpath('//body/div/p//text()').extract()
    	return item


