# -*- coding: utf-8 -*-
import scrapy
from ..items import AmazonwebscraperItem

class AmazonSpiderSpider(scrapy.Spider):
    name = 'amazon'
    page_number = 0
    max_pages = 1
    start_urls = [
            'https://www.amazon.es/s?bbn=599370031&rh=n%3A17425698031&brr=1&pd_rd_r=f7665802-112d-4aa6-a067-6f86311b8433&pd_rd_w=tsGEf&pd_rd_wg=GvZaY&rd=1&ref=Oct_d_odnav_599370031']
    def parse(self, response):
        AmazonSpiderSpider.page_number += 1
        items = AmazonwebscraperItem()

        all_page_products = response.css('.s-widget-spacing-small .sg-col-inner')

        for product in all_page_products:
            product_name = product.css('.a-color-base.a-text-normal').css('::text').extract()
            product_rating = product.css('.aok-align-bottom , .widgetId\=search-results_28 .a-icon-popover').css('::text').extract()
            product_price = product.css('.a-price-whole::text').extract()
            product_views = product.css('.a-size-small .a-size-base').css('::text').extract()
            product_imagelink = product.css('.s-image-square-aspect img::attr(src)').extract()

            items['product_name'] = product_name
            items['product_rating'] = product_rating
            items['product_price'] = product_price
            items['product_views'] = product_views
            items['product_imageLink'] = product_imagelink

            yield items

        next_page = 'https://www.amazon.es/s?i=electronics&bbn=599370031&rh=n%3A17425698031&page='+str(AmazonSpiderSpider.page_number)+'&brr=1&pd_rd_r=f7665802-112d-4aa6-a067-6f86311b8433&pd_rd_w=tsGEf&pd_rd_wg=GvZaY&qid=1637710604&rd=1&ref=sr_pg_'+str(AmazonSpiderSpider.page_number)

        if AmazonSpiderSpider.page_number < AmazonSpiderSpider.max_pages:
            yield response.follow(next_page, callback=self.parse)
