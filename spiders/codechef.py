import scrapy
from scrapy_playwright.page import PageMethod

class CodechefSpider(scrapy.Spider):
    name = "codechef"

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.codechef.com/users/blazze",
            callback=self.parse,
            meta={
                "playwright": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", "table.dataTable")
                ],
            },
        )

    def parse(self, response):
        data = []
        for row in response.css("table.dataTable > tbody > tr"):
            
            problem = row.css("td:nth-child(2) a::text").get()
            
            result = row.css("td:nth-child(3) span::attr(title)").get()
           

            data.append({
                "problem": problem,
                "result": result,
                
                
            })

        yield {"data": data}
