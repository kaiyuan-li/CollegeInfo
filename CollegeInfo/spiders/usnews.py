# -*- coding: utf-8 -*-
import scrapy
from CollegeInfo.items import scrapedInfo

class UsnewsSpider(scrapy.Spider):
    name = 'usnews'
    allowed_domains = ['https://www.usnews.com']

    def start_requests(self):
        yield scrapy.Request(
            url = 'https://www.usnews.com/best-colleges/rankings/national-universities',
            callback = self.parse
        )

    def parse(self, response):
        for infoDiv in response.css('div.shadow-dark.block-flush'):
            college = scrapedInfo()
            college['site'] = 'USNews'
            college['name'] = infoDiv.css('h3.heading-large.block-tighter > a::text').extract_first()
            college['rank'] = infoDiv.css('div.text-strong > div::text').extract_first().strip()
            if college['rank'] is None:
                college['rank'] = infoDiv.css('div.block-normal.text-strong').extract_first().strip()
            college['location'] = infoDiv.css('div.block-normal.text-small::text').extract_first().strip()
            college['cost'] = infoDiv.css('div.display-inline-for-medium-up.inline-right-tight-for-medium-up.border-right-for-medium-up > strong::text').extract_first()
            college['icon'] = infoDiv.css('div.right > a::attr(href)').extract_first()
            if college['icon'] is not None:
                college['icon'] = self.allowed_domains[0] + college['icon']
            college['link'] = infoDiv.css('h3.heading-large.block-tighter > a::attr(href)').extract_first()
            if college['link'] is not None:
                college['link'] = self.allowed_domains[0] + infoDiv.css('h3.heading-large.block-tighter > a::attr(href)').extract_first()
            yield college

        next_page = response.css('link[rel="next"]::attr(href)').extract_first()
        if 'page=11' not in next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse, dont_filter=True)