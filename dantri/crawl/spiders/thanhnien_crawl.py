import scrapy
from scrapy import Request


class NewsSpider(scrapy.Spider):
    name = "thanhnien_crawl"

    start_urls = [
        'https://thanhnien.vn/van-hoa/'
    ]

    count = 0
    MAX_COUNT = 2000

    def parse(self, response):
        urls = response.css(".cate-content .zone--timeline article.story h2 a::attr(href)").getall()
        next_page = response.css("nav#paging ul li.active + li a::attr(href)").get()
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
        title = response.css("#storybox h1.details__headline::text").get()
        contents = response.css(
            "div#storybox.details div#main_detail.clearfix div#abody div:not(.details__morenews)::text").getall()

        f = open("data_thanh_nien.txt", mode="a", encoding="UTF8")
        f.write(title.strip() + '. ')
        for content in contents:
            f.write(content.strip())
        f.write('\n')
        f.close()
