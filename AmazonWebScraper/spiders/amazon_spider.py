# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

from ..items import AmazonPhoneItem


class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    base_url = 'https://www.amazon.es'
    page_number = 0
    max_pages = 2
    start_urls = [
        'https://www.amazon.es/s?bbn=599370031&rh=n%3A17425698031&brr=1&pd_rd_r=f7665802-112d-4aa6-a067-6f86311b8433'
        '&pd_rd_w=tsGEf&pd_rd_wg=GvZaY&rd=1&ref=Oct_d_odnav_599370031']

    def parse(self, response):
        AmazonSpider.page_number += 1
        phones = AmazonPhoneItem()

        all_page_products = response.css('.s-widget-spacing-small .sg-col-inner')

        for product in all_page_products:

            description = product.css('.a-color-base.a-text-normal').css('::text').get()
            product_rating = product.css('.aok-align-bottom , .widgetId\=search-results_28 .a-icon-popover').css(
                '::text').get()
            product_price = product.css('.a-price-whole::text').get()
            product_views = product.css('.a-size-small .a-size-base').css('::text').get()
            product_imagelink = product.css('.s-image-square-aspect img::attr(src)').get()

            phones['description'] = description
            phones['rating'] = product_rating
            phones['price'] = product_price
            phones['views'] = product_views
            phones['image'] = product_imagelink

            phone_page = AmazonSpider.base_url + str(product.css('.s-line-clamp-4 a::attr(href)').get())
            yield Request(url=phone_page, callback=self.parse_page2, meta={'phones': phones})


        next_page = 'https://www.amazon.es/s?i=electronics&bbn=599370031&rh=n%3A17425698031&page=' + str(
            AmazonSpider.page_number) + '&brr=1&pd_rd_r=f7665802-112d-4aa6-a067-6f86311b8433&pd_rd_w=tsGEf' \
                                              '&pd_rd_wg=GvZaY&qid=1637710604&rd=1&ref=sr_pg_' + str(
            AmazonSpider.page_number)

        if AmazonSpider.page_number < AmazonSpider.max_pages:
            yield Request(next_page, callback=self.parse, dont_filter=True)

    def parse_page2(self, response):

        phones = response.meta['phones']
        phone_product = response.css('a-normal a-spacing-micro')

        brand = phone_product.css('.po-brand .a-span9 .a-size-base').css('::text').get()

        phones['brand'] = 'cheese'

        yield phones

