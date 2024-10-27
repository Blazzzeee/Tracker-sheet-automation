import scrapy
from scrapy_playwright.page import PageMethod

class CodechefSpider(scrapy.Spider):
    name = "codechef"
    allowed_domains = ["codechef.com"]
    start_urls = ["https://codechef.com/"]

    def start_requests(self):
        
        yield scrapy.Request(
            url="https://www.codechef.com/users/vashuvats1",
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
            
            if result=="accepted":
                data.append({
                    "problem": problem,
                    "result": result,
                })
            # else:
            #     data.append({
            #     "DEBUG: ":problem+result
                    
            #     })

        yield {"data": data}
