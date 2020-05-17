import scrapy
from scrapy import Request


class NewsSpider(scrapy.Spider):
    name = "dantri_crawl"

    start_urls = [
        'https://dantri.com.vn/tinh-yeu-gioi-tinh.htm'
    ]

    count = 0
    MAX_COUNT = 10


    def parse(self, response):
        urls = response.css("div[data-boxtype=timelineposition] .mr1 h2 a::attr(href)").getall()
        next_page = response.css(".container .clearfix .clearfix.mt1 .fr a::attr(href)").get()
        for url in urls:
            if self.count < self.MAX_COUNT:
                news_url = response.urljoin(url)
                yield Request(news_url, self.parse_content)
            else:
                break

        if next_page is not None and self.count < self.MAX_COUNT:
            next_page_url = response.urljoin(next_page)
            yield Request(next_page_url, self.parse)

    def parse_content(self, response):
        self.count += 1
        title = response.css("h1.fon31.mgb15::text").get()
        span = response.css("h2.fon33.mt1.sapo::text").get()
        contents = response.css("#divNewsContent p::text").getall()
        f = open("dantri_data.txt", mode="a", encoding="utf-8")
        f.write(title.strip() + '. ')
        f.write(span.strip() + '. ')
        for content in contents:
            f.write(content.strip())
            f.write('\n')
        f.write('\n\n')
