# -*- coding: utf-8 -*-
import scrapy
from ..items import AmazonwebscraperItem

class AmazonSpiderSpider(scrapy.Spider):
    name = 'amazon'
    page_number = 2
    start_urls = [
            'https://www.amazon.es/s?bbn=599370031&rh=n%3A17425698031&brr=1&pd_rd_r=f7665802-112d-4aa6-a067-6f86311b8433&pd_rd_w=tsGEf&pd_rd_wg=GvZaY&rd=1&ref=Oct_d_odnav_599370031']

    def parse(self, response):
        AmazonSpiderSpider.page_number += 1;
        items = AmazonwebscraperItem()

        product_name = response.css('.a-color-base.a-text-normal').css('::text').extract()
        product_rating = response.css('.aok-align-bottom , .widgetId\=search-results_28 .a-icon-popover').css('::text').extract()
        product_price = response.css('.a-price-whole::text').extract()
        product_views = response.css('.a-size-small .a-size-base').css('::text').extract()
        product_imagelink = response.css('.s-image-square-aspect img::attr(src)').extract()

        items['product_name'] = product_name
        items['product_rating'] = product_rating
        items['product_price'] = product_price
        items['product_views'] = product_views
        items['product_imageLink'] = product_imagelink

        yield items

        next_page = 'https://www.amazon.es/s?i=electronics&bbn=599370031&rh=n%3A17425698031&page='+str(AmazonSpiderSpider.page_number)+'&brr=1&pd_rd_r=f7665802-112d-4aa6-a067-6f86311b8433&pd_rd_w=tsGEf&pd_rd_wg=GvZaY&qid=1637710604&rd=1&ref=sr_pg_'+str(AmazonSpiderSpider.page_number)

        if AmazonSpiderSpider.page_number <= 20:
            yield response.follow(next_page, callback=self.parse)
