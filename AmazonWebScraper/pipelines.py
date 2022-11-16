# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import locale
import re

from elasticsearch import Elasticsearch

from AmazonWebScraper.settings import ELASTICSEARCH_PASSWORD, ELASTICSEARCH_USER, ELASTICSEARCH_URL


def parse_memory_storage(memory_storage):
    if not memory_storage:
        return memory_storage
    try:
        return locale.atof(re.findall(r'\b\d+\b', str(memory_storage))[0])
    except Exception as err:
        print('Cannot convert [memory_storage] field. Value: {' + memory_storage + '}. Error ' + str(err))
        return float(0)


def parse_price(price):
    if not price:
        return price
    try:
        print(price)
        return locale.atof(re.sub("[$|€]", "", str(price)))
    except Exception as err:
        print('Cannot convert [price] field. Value: {' + price + '}. Error: ' + str(err))
        return float(0)


def parse_rating(rating):
    if not rating:
        return 0
    try:
        return locale.atof(str(rating).split(' de 5 estrellas')[0])
    except Exception as err:
        print('Cannot convert [memory_storage] field. Value: {' + rating + '}. Error ' + str(err))
        return float(0)


def parse_screen_size(screen_size):
    if not screen_size:
        return screen_size
    try:
        return float(str(screen_size).split(' Pulgadas')[0])
    except Exception as err:
        print('Cannot convert [memory_storage] field. Value: {' + screen_size + '}. Error ' + str(err))
        return float(0)


def parse_views(views):
    if not views:
        return 0
    try:
        if ' valoraciones' not in views:
            return 0
        return int(str(views).split(' valoraciones')[0])
    except Exception as err:
        print('Cannot convert [memory_storage] field. Value: {' + views + '}. Error ' + str(err))
        return 0


class AmazonwebscraperPipeline(object):
    locale.setlocale(locale.LC_NUMERIC, "es_ES")

    def open_spider(self, spider):
        try:

            # Connection to Elasticsearch
            es = Elasticsearch(ELASTICSEARCH_URL, http_auth=(ELASTICSEARCH_USER, ELASTICSEARCH_PASSWORD),
                               verify_certs=False)
            print("Connection to Elasticsearch successfully established!. Info " + str(es.info()))

            if es.indices.exists(index="riws_amazon_scraper"):
                print("Index already exists")
                es.indices.delete(index='riws_amazon_scraper', ignore=[400, 404])
            # Create index in Elasticsearch
            try:
                settings = {
                    "mappings": {
                        "properties": {
                            "brand": {
                                "type": "keyword",
                            },
                            "model_name": {
                                "type": "text",
                            },
                            "rating": {
                                "type": "double",
                            },
                            "price": {
                                "type": "double",
                            },
                            "number_ratings": {
                                "type": "integer",
                            },
                            "image": {
                                "type": "text",
                                "index": "false"
                            },
                            "os": {
                                "type": "keyword",
                            },
                            "cellular_technology": {
                                "type": "keyword",
                            },
                            "memory_storage": {
                                "type": "keyword",
                            },
                            "connectivity": {
                                "type": "text",
                            },
                            "color": {
                                "type": "text",
                            },
                            "screen_size": {
                                "type": "double",
                            },
                            "wireless_net_tech": {
                                "type": "text",
                            },
                            "full": {
                                "type": "text",
                            }
                        }
                    }
                }

                es.indices.create(index='riws_amazon_scraper', body=settings)
                print("Index successfully created!")
            except Exception as index_err:
                print("Couldn't create index in Elasticsearch. Error " + str(index_err))

        except Exception as err:
            print("Couldn't connect to Elasticsearch. Error " + str(err))

    def process_item(self, item, spider):
        try:
            es = Elasticsearch(ELASTICSEARCH_URL, http_auth=(ELASTICSEARCH_USER, ELASTICSEARCH_PASSWORD),
                               verify_certs=False)
            doc = {
                "brand": str(item['brand']),
                "model_name": str(item['model_name']),
                "rating": parse_rating(str(item['rating'])),
                "price": parse_price(str(item['price'])),
                "number_ratings": parse_views(str(item['views'])),
                "image": str(item['image']),
                "os": str(item['os']),
                "cellular_technology": str(item['cellular_technology']),
                "memory_storage": str(item['memory_storage']),
                "connectivity": str(item['connectivity']),
                "color": str(item['color']),
                "screen_size": parse_screen_size(str(item['screen_size'])),
                "wireless_net_tech": str(item['wireless_net_tech']),
                "full": str(item['brand']) + " " + str(item['model_name']) + " " + str(item['rating']) + " " + str(
                    item['price']) + " " + str(
                    item['views']) + " " + str(item['os']) + " " + str(item['cellular_technology']) + " " + str(
                    item['memory_storage']) + " " + str(item['connectivity']) + " " + str(item['color']) + " " + str(
                    item['screen_size']) + " " + str(item['wireless_net_tech'])
            }

            if item['brand'] and item['os'] and item['cellular_technology'] and item['memory_storage']:
                es.index(index="riws_amazon_scraper", document=doc)
        except Exception as err:
            print("Couldn't connect to Elasticsearch in indexing item " + str(item) + ". Error " + str(err))

        return item
