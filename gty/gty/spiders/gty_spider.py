import scrapy

class GtySpider(scrapy.Spider):
    name = "gty"
    allowed_domains = ["gty.org"]
    start_urls = [
        "http://www.gty.org/resources/sermons/scripture/daniel"
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
