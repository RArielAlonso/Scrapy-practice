import scrapy


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        all_books = response.xpath('//article[@class="product_pod"]')
        for book in all_books:
            book_url = book.xpath('.//h3/a/@href').extract_first()
            if "catalogue/" not in book_url:
                book_url='catalogue/'+book_url
            book_url=self.start_urls[0]+book_url
            yield scrapy.Request(book_url, callback=self.parse_book)
        
        next_page_partial_url=response.xpath('//li[@class="next"]//a/@href').extract_first()
        if next_page_partial_url:
            if 'catalogue/' not in next_page_partial_url:
                next_page_partial_url='catalogue/'+next_page_partial_url
            next_page_url=self.start_urls[0]+next_page_partial_url
            yield scrapy.Request(next_page_url, callback=self.parse)
        
    def parse_book(self, response):
        title = response.xpath('//div/h1/text()').extract_first()
        #print(title)
        relative_image=response.xpath('//div[@class="item active"]//@src').extract_first()
        final_image = self.start_urls[0] + relative_image.replace('../..', '')
        #print(final_image)
        price = response.xpath(
            '//div[contains(@class, "product_main")]/p[@class="price_color"]/text()').extract_first()
        #print(price)
        stock = response.xpath(
            '//div[contains(@class, "product_main")]/p[contains(@class, "instock")]/text()').extract()[1].strip()
        #print(stock)
        star_rating=response.xpath(
            '//div[contains(@class, "product_main")]//p[contains(@class,"star-rating")]//@class').extract_first().replace('star-rating ','')
        #print(star_rating)
        description = response.xpath(
            '//div[@id="product_description"]/following-sibling::p/text()').extract_first()
        #print(description)
        upc = response.xpath(
            '//table[@class="table table-striped"]/tr[1]/td/text()').extract_first()
        #print(upc)
        price_exl_tax=response.xpath('//table[@class="table table-striped"]//tr[3]//td/text()').extract_first()
        #print(price_exl_tax)
        price_inc_tax=response.xpath('//table[@class="table table-striped"]//tr[4]//td/text()').extract_first()
        #print(price_inc_tax)
        tax=response.xpath('//table[@class="table table-striped"]//tr[5]//td/text()').extract_first()
        #print(tax)
        yield{
            'Title': title,
            'Image': final_image,
            'Price': price,
            'Stock': stock,
            'Stars': star_rating,
            'Description': description,
            'Upc': upc,
            'Price excl tax': price_exl_tax,
            'Price incl tax': price_inc_tax,
            'Tax': tax,
        }