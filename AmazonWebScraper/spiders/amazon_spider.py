# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

from ..items import AmazonPhoneItem


class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    base_url = 'https://www.amazon.es'
    page_number = 0
    max_pages = 20
    start_urls = [
        'https://www.amazon.es/s?i=electronics&bbn=599370031&rh=n%3A17425698031&page=4&brr=1&pd_rd_r=f7665802-112d-4aa6-a067-6f86311b8433%27%27&pd_rd_w=tsGEf&pd_rd_wg=GvZaY&qid=1668634648&rd=1&ref=sr_pg_4']

    def parse(self, response):
        AmazonSpider.page_number += 1

        products = response.css('.s-widget-spacing-small .sg-col-inner')

        for product in products:
            product_link = AmazonSpider.base_url + str(product.css('.s-line-clamp-4 a::attr(href)').get())
            yield response.follow(product_link, callback=self.parse_products)

        next_page = 'https://www.amazon.es/s?i=electronics&bbn=599370031&rh=n%3A17425698031&page=' + str(
            AmazonSpider.page_number) + '&brr=1&pd_rd_r=f7665802-112d-4aa6-a067-6f86311b8433&pd_rd_w=tsGEf' \
                                        '&pd_rd_wg=GvZaY&qid=1637710604&rd=1&ref=sr_pg_' + str(
            AmazonSpider.page_number)

        if AmazonSpider.page_number < AmazonSpider.max_pages:
            yield Request(next_page, callback=self.parse, dont_filter=True)

    def parse_products(self, response):

        phones = AmazonPhoneItem()

        brand = response.css('.po-brand .a-span9 .a-size-base').css('::text').get()
        model_name = response.css('.po-model_name .a-span9 .a-size-base').css('::text').get()
        os = response.css('.po-operating_system .a-span9 .a-size-base').css('::text').get()
        cellular_tech = response.css('.po-cellular_technology .a-span9 .a-size-base').css('::text').get()
        memory_storage = response.css('.po-memory_storage_capacity .a-span9 .a-size-base').css('::text').get()
        connectivity = response.css('.po-connectivity_technology .a-span9 .a-size-base').css('::text').get()
        color = response.css('.po-color .a-span9 .a-size-base').css('::text').get()
        screen_size = response.css('.po-display\.size .a-span9 .a-size-base').css('::text').get()
        wireless_net_tech = response.css('.po-wireless_network_technology .a-span9 .a-size-base').css('::text').get()
        rating = response.css('.a-icon-alt').css('::text').get()
        image = response.css('#imgTagWrapperId img::attr(src)').get()
        price = response.css('.a-offscreen').css('::text').get()
        views = response.css('.a-declarative .a-link-normal .a-size-base').css('::text').get()

        phones['views'] = views
        phones['price'] = price
        phones['image'] = image
        phones['rating'] = rating
        phones['brand'] = brand
        phones['model_name'] = model_name
        phones['os'] = os
        phones['cellular_technology'] = cellular_tech
        phones['memory_storage'] = memory_storage
        phones['connectivity'] = connectivity
        phones['color'] = color
        phones['screen_size'] = screen_size
        phones['wireless_net_tech'] = wireless_net_tech

        yield phones
