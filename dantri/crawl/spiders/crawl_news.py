import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request


class DantriCrawler(CrawlSpider):
    name = "crawler"
    allowed_domains = ['dantri.com.vn']
    start_urls = ['https://dantri.com.vn/van-hoa.htm']

    count = 0
    MAX_COUNT = 20

    rules = (
        Rule(
            link_extractor=LinkExtractor(allow=()),
            callback='parse',
            follow=True
        ),
    )

    def parse(self, response):
        urls = response.css("div[data-boxtype=timelineposition] .mr1 h2 a::attr(href)").getall()
        next_page = response.css(".container .clearfix .clearfix.mt1 .fr a::attr(href)").get()
        for url in urls:
            if self.count < self.MAX_COUNT:
                self.count += 1
                news_content_url = response.urljoin(url)
                yield Request(news_content_url, self.parse_content)
            else:
                break

        if next_page is not None and self.count < self.MAX_COUNT:
            next_page_url = response.urljoin(next_page)
            yield Request(next_page_url, self.parse)

    def parse_content(self, response):
        title = response.css("h1.fon31.mgb15::text").get()
        span = response.css("h2.fon33.mt1.sapo::text").get()
        contents = response.css("#divNewsContent p::text").getall()

        f = open("data.txt", mode="a", encoding="UTF8")
        f.write(title.strip())
        f.write('.')
        f.write(span.strip())
        f.write('.')
        for content in contents:
            f.write(content.strip())
        f.write('\n')
        f.write('\n')
