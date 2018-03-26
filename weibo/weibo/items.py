# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboItem(scrapy.Item):
    url = scrapy.Field()
    id = scrapy.Field()
    content = scrapy.Field()
    comment_count = scrapy.Field()
    forward_count = scrapy.Field()
    like_count = scrapy.Field()
    posted_time = scrapy.Field()
    user = scrapy.Field()
