import scrapy
from scrapy import Request
from ..items import VnexpressItem


class VNEpress(scrapy.Spider):
	name = "vnexpress"
	start_urls = [
		"https://vnexpress.net/doi-song"
	]
	count = 0
	MAX_COUNT = 10000


	def parse(self, response):
		urls = response.css("article[class=list_news] .description a::attr(href)").getall()
		next_page = response.css(".container .sidebar_1 .pagination.mb10 .pagination_btn.pa_next.next ::attr(href)").get()
		for url in urls:
			if self.count < self.MAX_COUNT:
				connect_to_url = response.urljoin(url)
				yield Request(connect_to_url, callback=self.parse_content)
			else:
				break
		if next_page is not None and self.count < self.MAX_COUNT:
			next_url = response.urljoin(next_page)
			yield Request(next_url, callback=self.parse)


	def parse_content(self, response):
		self.count += 1
		item = VnexpressItem()
		title = response.xpath('//*[@id="col_sticky"]/p/text()').get()
		if title != None:
			item["title"] = title.strip()
			yield item
