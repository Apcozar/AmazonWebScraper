# -*- coding: utf-8 -*-
import scrapy
from ..items import AmazonPhoneItem


class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    base_url = 'https://www.amazon.es'
    page_number = 0
    max_pages = 1
    start_urls = [
        'https://www.amazon.es/s?bbn=599370031&rh=n%3A17425698031&brr=1&pd_rd_r=f7665802-112d-4aa6-a067-6f86311b8433'
        '&pd_rd_w=tsGEf&pd_rd_wg=GvZaY&rd=1&ref=Oct_d_odnav_599370031']

    def parse(self, response):
        AmazonSpider.page_number += 1
        items = AmazonPhoneItem()

        all_page_products = response.css('.s-widget-spacing-small .sg-col-inner')

        for product in all_page_products:
            link = AmazonSpider.base_url + str(product.css('.s-line-clamp-4 a::attr(href)').get())
            model_name = product.css('.a-color-base.a-text-normal').css('::text').get()
            product_rating = product.css('.aok-align-bottom , .widgetId\=search-results_28 .a-icon-popover').css(
                '::text').get()
            product_price = product.css('.a-price-whole::text').get()
            product_views = product.css('.a-size-small .a-size-base').css('::text').get()
            product_imagelink = product.css('.s-image-square-aspect img::attr(src)').get()

            items['model_name'] = model_name
            items['rating'] = product_rating
            items['price'] = product_price
            items['views'] = product_views
            items['image'] = product_imagelink
            items['link'] = link
            yield items

        next_page = 'https://www.amazon.es/s?i=electronics&bbn=599370031&rh=n%3A17425698031&page=' + str(
            AmazonSpider.page_number) + '&brr=1&pd_rd_r=f7665802-112d-4aa6-a067-6f86311b8433&pd_rd_w=tsGEf' \
                                              '&pd_rd_wg=GvZaY&qid=1637710604&rd=1&ref=sr_pg_' + str(
            AmazonSpider.page_number)

        if AmazonSpider.page_number < AmazonSpider.max_pages:
            yield response.follow(next_page, callback=self.parse)
