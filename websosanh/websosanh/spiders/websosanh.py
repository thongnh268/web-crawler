import scrapy
from scrapy import Request
from ..items import WebsosanhItem

class Websosanh(scrapy.Spider):

	name = "websosanh"
	allowed_domains = ["websosanh.vn"]
	start_urls = ["https://websosanh.vn/dan-organ/cat-2022.htm"]
	count = 0
	MAX_PAGE = 100


	def parse(self, response):
		urls = response.css('div[id=productListByType] .list-item.list-product-search li .img-wrap.lazyload a::attr(href)').getall()
		next_page = response.css(".list-type-grid .pagination.pull-right.mt0 li .next ::attr(href)").get()
		for url in urls:
			self.count += 1
			if self.count < self.MAX_PAGE:
				connect_to_url = response.urljoin(url)
				yield Request(connect_to_url, callback=self.parse_items)
			else:
				break
		if next_page is not None and self.count < self.MAX_PAGE:
			next_url = response.urljoin(next_page)
			yield Request(next_url, callback=self.parse)

	def parse_items(self, response):
		item = WebsosanhItem()
		title = response.css(".container-fluid .container .page-detail.row div h1 ::text").get()
		prices = response.css(".table .col-price.text-center .price::text").getall()
		links = response.css(".table .col-product-info h3 a ::attr(href)").getall()
		prices = [p for p in prices if p.strip() != ""]
		# locations = response.css(".table .col-product-info .location-wrap span ::text").getall()
		details = {}
		for i, c in enumerate(links):
			details["link_{}".format(i+1)] = {
			"link": links[i].strip(),
			"price": prices[i].strip()
			}
		# 	if locations[i] != None:

		item["name"] = title.strip()
		item["detail"] = details
		# print(item["name"], item["detail"], end="===============")
		yield item
		# print(len(locations), len(links))
		# print(len(locations), len(prices), len(links), end="============================")