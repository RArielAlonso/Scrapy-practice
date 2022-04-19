import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import BooksItem


class SpiderSpider(CrawlSpider):
    name = "crawl-spider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]
    rules = [
        Rule(
            LinkExtractor(allow="catalogue/"), callback="parse_filter_book", follow=True
        )
    ]

    def parse_filter_book(self, response):
        exists = response.xpath('//div[@id="product_gallery"]').extract_first()
        if exists:
            title = response.xpath("//div/h1/text()").extract_first()
            # print(title)
            relative_image = response.xpath(
                '//div[@class="item active"]//@src'
            ).extract_first()
            final_image = self.start_urls[0] + relative_image.replace("../..", "")
            # print(final_image)
            price = response.xpath(
                '//div[contains(@class, "product_main")]/p[@class="price_color"]/text()'
            ).extract_first()
            # print(price)
            stock = (
                response.xpath(
                    '//div[contains(@class, "product_main")]/p[contains(@class, "instock")]/text()'
                )
                .extract()[1]
                .strip()
            )
            # print(stock)
            star_rating = (
                response.xpath(
                    '//div[contains(@class, "product_main")]//p[contains(@class,"star-rating")]//@class'
                )
                .extract_first()
                .replace("star-rating ", "")
            )
            # print(star_rating)
            description = response.xpath(
                '//div[@id="product_description"]/following-sibling::p/text()'
            ).extract_first()
            # print(description)
            upc = response.xpath(
                '//table[@class="table table-striped"]/tr[1]/td/text()'
            ).extract_first()
            # print(upc)
            price_exl_tax = response.xpath(
                '//table[@class="table table-striped"]//tr[3]//td/text()'
            ).extract_first()
            # print(price_exl_tax)
            price_inc_tax = response.xpath(
                '//table[@class="table table-striped"]//tr[4]//td/text()'
            ).extract_first()
            # print(price_inc_tax)
            tax = response.xpath(
                '//table[@class="table table-striped"]//tr[5]//td/text()'
            ).extract_first()
            # print(tax)
            book = BooksItem()

            book["title"] = title
            book["final_image"] = final_image
            book["price"] = price
            book["stock"] = stock
            book["stars"] = star_rating
            book["description"] = description
            book["tax"] = tax
            yield book
        else:
            print(response.url)
