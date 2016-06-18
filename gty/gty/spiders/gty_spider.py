import scrapy

from scrapy.http.request.form import FormRequest
from dateutil.parser import parse as parse_date

from gty.items import SermonItem


class GtySpider(scrapy.Spider):
    name = "gty"
    allowed_domains = ["gty.org"]
    start_urls = [
        "http://www.gty.org/resources/sermons"
    ]

    def parse(self, response):
        for sel in response.xpath('//div[@id="ctl00_ctl00_MainContent_SubMain_pnlFilterList"]/ul/li'):
            url = "http://gty.org%s" % (sel.xpath('a/@href').extract()[0])
            yield scrapy.Request(url, callback=self.parse_book)

    def parse_book(self, response):
        book = response.url.split("/")[-1]
        for sel in response.xpath('//table[@id="ctl00_ctl00_MainContent_SubMain_gvTitles"]/tr[not(@class="paging")]/td/li'):
            sermon = SermonItem()
            sermon['book'] = book
            sermon['title'] = (sel.xpath('h5/a/text()').extract() or [None])[0]
            date_preached_val = (sel.xpath('p[1]/strong[@class="title"]/text()').extract() or [None])[0]
            date_preached = parse_date(date_preached_val) if date_preached_val else None
            sermon['date_preached'] = date_preached.strftime("%Y-%m-%d") if date_preached else ''
            sermon['scripture'] = (sel.xpath('p[1]/strong[@class="date"]/text()').extract() or [None])[0]
            sermon['ref'] = (sel.xpath('p[1]/text()').extract() or [None])[1]
            sermon['link'] = (sel.xpath('p[2]/strong[@class="date"]/a/@href').extract() or [None])[0]
            yield sermon

        viewstate = response.xpath("//input[@id='__VIEWSTATE']/@value").extract().pop()
        pages = response.xpath('//table[@id="ctl00_ctl00_MainContent_SubMain_gvTitles"]/tr[@class="paging"][1]/td/table/tr/td')
        current_page_elems = pages.xpath('span/text()').extract()
        if len(current_page_elems) > 0:
            current_page = int(current_page_elems[0])
            next_page = current_page + 1
            if next_page <= len(pages):
                argument = u"Page$%s" % str(next_page)
                data = {'__EVENTTARGET': u"ctl00$ctl00$MainContent$SubMain$gvTitles", '__EVENTARGUMENT': argument, '__LASTFOCUS': u'', '__EVENTVALIDATION': u'', '__VIEWSTATE': viewstate}
                yield FormRequest(response.url, formdata=data, callback=self.parse_book)
