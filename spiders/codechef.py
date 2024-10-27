import scrapy
from scrapy_playwright.page import PageMethod

class CodechefSpider(scrapy.Spider):
    name = "codechef"
    allowed_domains = ["codechef.com"]
    start_urls = ["https://www.codechef.com/users/vashuvats1"]
    pages = 0

    def start_requests(self):
        # Start with maxpage request
        yield scrapy.Request(
            url="https://www.codechef.com/recent/user?page=0&user_handle=vashuvats1",
            callback=self.maxpage
        )

    def maxpage(self, response):
        # Debug log
        print("DEBUG LOG: maxpages called")
        self.pages = 1  # Dummy assignment for demonstration
        print(f"DEBUG LOG: pages {self.pages}")
        
        # Proceed to main user page request
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

            if result == "accepted":
                data.append({
                    "problem": problem,
                    "result": result,
                })

        yield {"data": data}
