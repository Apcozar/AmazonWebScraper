# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from elasticsearch import Elasticsearch
from AmazonWebScraper.settings import ELASTICSEARCH_PASSWORD, ELASTICSEARCH_USER, ELASTICSEARCH_URL

# Single node via URL


class AmazonwebscraperPipeline(object):

    def open_spider(self, spider):
        try:
            # Connection to Elasticsearch
            elasticsearch = Elasticsearch(ELASTICSEARCH_URL, http_auth=(ELASTICSEARCH_USER, ELASTICSEARCH_PASSWORD),
                                          verify_certs=False)
            print("Connection to Elasticsearch successfully established!. Info " + str(elasticsearch.info()))

            if elasticsearch.indices.exists(index="riws_amazon_scraper"):
                print("Index already exists")
            else:
                # Create index in Elasticsearch
                try:
                    mapping = {
                        "mappings": {
                            "properties": {
                                "image": {
                                    "type": "text",
                                    "index": "false"
                                }
                            }
                        }
                    }

                    elasticsearch.indices.create(index='riws_amazon_scraper', body=mapping)
                    print("Index successfully created!")
                except Exception as index_err:
                    print("Couldn't create index in Elasticsearch. Error " + str(index_err))

        except Exception as err:
            print("Couldn't connect to Elasticsearch. Error " + str(err))

    def process_item(self, item, spider):
        # TODO: Get items properties and create indexes in Elasticsearch

        return item
