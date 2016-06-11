import scrapy

class GtySpider(scrapy.Spider):
    name = "gty"
    allowed_domains = ["gty.org"]
    start_urls = [
        "http://www.gty.org/resources/sermons/scripture/daniel"
    ]

    def parse(self, response):
        for sel in response.xpath('//table[@id="ctl00_ctl00_MainContent_SubMain_gvTitles"]/tr[not(@class="paging")]/td/li'):
	    title = sel.xpath('h5/a/text()').extract()
            date_preached = sel.xpath('p[1]/strong[@class="title"]/text()').extract()
            scripture = sel.xpath('p[1]/strong[@class="date"]/text()').extract()
            ref = sel.xpath('p[1]/text()').extract()
            link = sel.xpath('p[2]/strong[@class="date"]/a/@href').extract()
            print("%s - %s - %s - %s - %s" % (title, date_preached, scripture, ref, link))
