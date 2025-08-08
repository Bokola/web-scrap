import scrapy
from scrapy.http import Response, Request


class ProductsSpider(scrapy.Spider):
    name = 'products'
    allowed_domains = ['web-scraping.dev']
    start_urls = [
        'https://web-scraping.dev/products',
    ]

    def parse(self, response: Response):
        product_urls = response.xpath(
            "//div[@class='row product']/div/h3/a/@href"
        ).getall()
        for url in product_urls:
            yield Request(url, callback=self.parse_product)
        # or shortcut in scrapy >2.0
        # yield from response.follow_all(product_urls, callback=self.parse_product)
    
    def parse_product(self, response: Response):
        print(response)


# populate parse_product()
    
    def parse_product(self, response: Response):
        yield {
            "title": response.xpath("//h3[contains(@class, 'product-title')]/text()").get(),
            "price": response.xpath("//span[contains(@class, 'product-price')]/text()").get(),
            "image": response.xpath("//div[contains(@class, 'product-image')]/img/@src").get(),
            "description": response.xpath("//p[contains(@class, 'description')]/text()").get()
        }


