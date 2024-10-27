import scrapy
import json

class CodechefSpider(scrapy.Spider):
    name = "static1"
    allowed_domains = ["codechef.com"]
    start_urls = ["https://www.codechef.com/"]
    # page=0
    def start_requests(self):
        yield scrapy.Request(
            url="https://www.codechef.com/recent/user?page=0&user_handle=vashuvats1",
            callback=self.parse,
        )

    def parse(self, response):
        json_data = json.loads(response.text)
        html_content = json_data.get("content", "")
        selector = scrapy.Selector(text=html_content)
        data = []
        for row in selector.css("table.dataTable > tbody > tr"):
            problem = row.css("td:nth-child(2) a::text").get()
            result = row.css("td:nth-child(3) span::attr(title)").get()
            if result == "accepted":
                data.append({
                    "problem": problem,
                    "result": result,
                })
        
        yield {"data": data}
