from typing import Iterable
import scrapy
from scrapy_playwright.page import PageMethod



class CodechefSpider(scrapy.Spider):
    name = "codechef"
    # allowed_domains = ["codechef.com"]
    # start_urls = ["https://codechef.com"]

    def start_requests(self):
        yield scrapy.Request(url="https://www.codechef.com/users/blazze",callback=self.parse,meta={
            "playwright":True,
            "playwright_include_page":True,
            # "playwright_page_methods": [PageMethod("wait_for_selector","div#rankContentDiv")]
        })
        

    async def parse(self, response):
        

        yield {"test1": response.css("div#rankContentDiv").get()}
