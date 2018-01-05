# -*- coding: utf-8 -*-
import scrapy
from CollegeInfo.items import scrapedInfo

class UsnewsSpider(scrapy.Spider):
    name = 'usnews'
    allowed_domains = ['https://www.usnews.com/best-colleges/rankings/national-universities']
    start_urls = ['https://www.usnews.com/best-colleges/rankings/national-universities']

    def parse(self, response):
        for infoDiv in response.css("div.shadow-dark.block-flush"):
            college = scrapedInfo()
            college["name"] = infoDiv.css("h3.heading-large.block-tighter a::text").extract_first()
            college["rank"] = infoDiv.css("div.text-strong div::text").extract_first().split()[0]
            if college["rank"] is None:
                college["rank"] = infoDiv.css("div.block-normal.text-strong").extract_first()
            college["site"] = "USNews"
            yield college

        next_page = response.css("link[rel='next']::attr(href)").extract_first()
        if "page=11" not in next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse, dont_filter=True)