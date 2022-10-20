# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from elasticsearch import Elasticsearch
from AmazonWebScraper.settings import ELASTICSEARCH_PASSWORD, ELASTICSEARCH_USER, ELASTICSEARCH_URL

class AmazonwebscraperPipeline(object):

    def open_spider(self, spider):
        try:
            
            # Connection to Elasticsearch
            es = Elasticsearch(ELASTICSEARCH_URL, http_auth=(ELASTICSEARCH_USER, ELASTICSEARCH_PASSWORD),
                                          verify_certs=False)
            print("Connection to Elasticsearch successfully established!. Info " + str(es.info()))

            if es.indices.exists(index="riws_amazon_scraper"):
                print("Index already exists")               
                es.indices.delete(index='riws_amazon_scraper', body=mapping)
            # Create index in Elasticsearch
            try:
                mapping = {
                    "mappings": {
                        "properties": {
                            "brand": {
                                "type": "text",
                            },
                            "model_name": {
                                "type": "text",
                            },
                            "rating": {
                                "type": "text",
                            },
                            "price": {
                                "type": "text",
                            },
                            "views": {
                                "type": "text",
                            },
                            # "image": {
                            #     "type": "text",
                            #     "index": "false"
                            # },
                            "os": {
                                "type": "text",
                            },
                            "cellular_technology": {
                                "type": "text",
                            },
                            "memory_storage": {
                                "type": "text",
                            },
                            "connectivity": {
                                "type": "text",
                            },
                            "color": {
                                "type": "text",
                            },
                            "screen_size": {
                                "type": "text",
                            },
                            # "description": {
                            #     "type": "text",
                            #     "index": "false"
                            # },
                            "wireless_net_tech": {
                                "type": "text",
                            }
                        }
                    }
                }

                es.indices.create(index='riws_amazon_scraper', body=mapping)
                print("Index successfully created!")
            except Exception as index_err:
                print("Couldn't create index in Elasticsearch. Error " + str(index_err))

        except Exception as err:
            print("Couldn't connect to Elasticsearch. Error " + str(err))

    def process_item(self, item, spider):
        # TODO: Get items properties and create indexes in Elasticsearch
        # Añadir al indice riws amazon scraper cada item como documento   
        try:
            es = Elasticsearch(ELASTICSEARCH_URL, http_auth=(ELASTICSEARCH_USER, ELASTICSEARCH_PASSWORD),
                                          verify_certs=False) 
           
            doc = {
                "brand" : str(item['brand']),
                "model_name" : str(item['model_name']),
                "rating" : str(item['rating']),
                "price" : str(item['price']),
                "views" : str(item['views']),
                #"image" : item.Image,
                "os" : str(item['os']),
                "cellular_technology" : str(item['cellular_technology']),
                "memory_storage" : str(item['memory_storage']),
                "connectivity" : str(item['connectivity']),
                "color" : str(item['color']),
                "screen_size" : str(item['screen_size']),
                #"description" : str(item['description']),
                "wireless_net_tech" : str(item['wireless_net_tech']),
            }
            print("Previo insert")

            resp = es.index(index="riws_amazon_scraper",document=doc)
        except Exception as err:
            print("Couldn't connect to Elasticsearch in insert. Error " + str(err))

        return item
