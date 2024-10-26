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
            time = row.css("td:nth-child(1) .tooltiptext::text").get()
            problem = row.css("td:nth-child(2) a::text").get()
            problem_title = row.css("td:nth-child(2) a::attr(title)").get()
            result = row.css("td:nth-child(3) span::attr(title)").get()
            language = row.css("td:nth-child(4)::text").get()
            solution_link = row.css("td:nth-child(5) a::attr(href)").get()

            data.append({
                "time": time,
                "problem": problem,
                "problem_title": problem_title,
                "result": result,
                "language": language,
                "solution_link": solution_link,
            })

        yield {"data": data}
