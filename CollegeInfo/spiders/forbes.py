# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from CollegeInfo.items import scrapedInfo

class ForbesSpider(scrapy.Spider):
    name = 'forbes'
    allowed_domains = ['https://www.forbes.com']
    custom_settings = {
        'SPLASH_URL': 'http://192.168.99.100:8050/',
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
        },
        'SPIDER_MIDDLEWARES': {
            'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
        },
        'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
    }

    def start_requests(self):
        script = """
        function main(splash, args)
            assert(splash:go(args.url))
            assert(splash:wait(1))
            assert(splash:runjs('document.querySelector("div.continue-button").click()'))
            assert(splash:wait(3))
            local num_scrolls = 10
            local scroll_to = splash:jsfunc('window.scrollTo')
            local get_body_height = splash:jsfunc('function() {return document.body.scrollHeight;}')

            for _ = 1, num_scrolls do
                scroll_to(0, get_body_height())
                splash:wait(1)
            end

            return {
                html = splash:html(),
            }
        end
        """

        yield scrapy.Request(
            url = 'https://www.forbes.com/top-colleges/list/',
            callback = self.parse,
            meta = {
                'splash': {
                    'args': {'lua_source': script},
                    'endpoint': 'execute',
                }
            }
        )

    def parse(self, response):
        for tableRow in response.css('table#the_list tbody tr.data')[:100]:
            college = scrapedInfo()
            college['site'] = 'Forbes'
            college['name'] = tableRow.css('td.name > a::text').extract_first()
            college['rank'] = tableRow.css('td.rank::text').extract_first()
            college['location'] = tableRow.css('td:nth-of-type(4)::text').extract_first()
            college['cost'] = tableRow.css('td:nth-of-type(5)::text').extract_first()
            college['icon'] = 'https:' + tableRow.css('td.image > a > img::attr(src)').extract_first()
            college['link'] = self.allowed_domains[0] + tableRow.css('td.image > a::attr(href)').extract_first()
            yield college