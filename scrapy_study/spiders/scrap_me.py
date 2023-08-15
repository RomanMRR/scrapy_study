import scrapy
from scrapy import Request
from scrapy_study.items import JsonXmlItem, ImageItem


class ScrapMeSpider(scrapy.Spider):
    name = 'scrap_me'
    start_urls = ['https://scrapeme.live/shop//']

    def parse(self, response):
        products = response.xpath('//a[contains(@class, "product__link")]')
        for product in products:
            item = JsonXmlItem()
            item['name'] = product.xpath('.//h2[contains(@class, "product__title")]/text()').get()
            item['price'] = product.xpath('.//span[contains(@class, "Price-amount")]/text()').get()
            yield item
        # Ищем ссылку на следующую страницу
        next_page = response.xpath("//a[@class='next page-numbers']/@href").get()
        if next_page:
            # И делаем к этой странице запрос, как если бы работали с простой ссылкой
            yield Request(url=next_page, callback=self.parse)


class ScrapMeSpiderImage(scrapy.Spider):
    name = 'scrap_me_image'
    start_urls = ['https://scrapeme.live/shop//']

    def parse(self, response):
        products = response.xpath('//a[contains(@class, "product__link")]')
        item = ImageItem()
        # Мы должны сформировать список из ссылок на картинки, обязательно должен быть список
        item['image_urls'] = []
        for product in products:
            item['image_urls'].append(product.xpath('.//img[contains(@class, "wp-post-image")]/@src').get())

        # Можно скачивать и одну картинку, главное класть её в список
        # item['image_urls'].append(products.xpath('//img[contains(@class, "wp-post-image")]/@src').get())
        yield item
