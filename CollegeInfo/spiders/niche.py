# -*- coding: utf-8 -*-
import scrapy
from CollegeInfo.items import scrapedInfo

class NicheSpider(scrapy.Spider):
    name = 'niche'
    allowed_domains = ['https://www.niche.com']

    def start_requests(self):
        yield scrapy.Request(
            url = 'https://www.niche.com/colleges/search/best-colleges/',
            callback = self.parse
        )

    def parse(self, response):
        for infoDiv in response.css('div.card > a.search-result__link'):
            college = scrapedInfo()
            college['site'] = 'Niche'
            college['name'] = infoDiv.css('div.card__inner > h2::text').extract_first()
            college['rank'] = infoDiv.css('div.card__inner > div.search-result-badge > span::text').extract_first()
            college['location'] = infoDiv.css('div.card__inner > ul.search-result-tagline > li:nth-of-type(2)::text').extract_first()
            college['cost'] = infoDiv.css('div.card__inner > ul.search-result-fact-list > li:nth-of-type(3) > div > span.search-result-fact__value::text').extract_first()
            college['link'] = infoDiv.css('::attr(href)').extract_first()
            yield college

        next_page = response.css('li.pagination__next > a::attr(href)').extract_first()
        if 'page=5' not in next_page:
        	yield scrapy.Request(next_page, callback=self.parse, dont_filter=True)