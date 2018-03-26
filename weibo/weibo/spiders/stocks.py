# -*- coding: utf-8 -*-

import re

import scrapy
from scrapy import FormRequest, Request

from atlednolispe_weibo import KEYWORD
from ..items import WeiboItem


class StocksSpider(scrapy.Spider):
    name = 'stocks'
    allowed_domains = ['weibo.cn']
    # start_urls = ['http://weibo.cn/']

    search_url = 'https://weibo.cn/search/mblog'
    max_page = 200

    def start_requests(self):
        keyword = KEYWORD
        url = '{url}?keyword={keyword}'.format(url=self.search_url, keyword=keyword)

        for page_num in range(self.max_page):
            data = {
                'mp': str(self.max_page),
                'page': str(page_num),
            }
            # yield FormRequest(url, callback=self.parse_list, formdata=data, cookies=COOKIES)  # cookies要单独加不能放在headers中
            yield FormRequest(url, formdata=data, callback=self.parse_list)

    def parse_list(self, response):
        weibos = response.xpath('//*[starts-with(@id, "M_")]')
        for weibo in weibos:
            is_forward = bool(weibo.xpath('.//span[@class="cmt"]').extract_first())
            if is_forward:
                detail_url = weibo.xpath('.//a[contains(., "原文评论[")]//@href').extract_first()
            else:
                detail_url = weibo.xpath('.//a[contains(., "评论[")]//@href').extract_first()
            yield Request(detail_url, callback=self.parse_detail)
            # print(detail_url)

    def parse_detail(self, response):
        url = response.url
        content = ''.join(response.xpath('//div[@id="M_"]//span[@class="ctt"]//text()').extract())
        id = re.search('comment/(.*?)\?', response.url).group(1)
        comment_count = response.xpath('//span[@class="pms"]//text()').re_first('评论\[(.*?)\]')
        forward_count = response.xpath('//a[contains(., "转发[")]//text()').re_first('转发\[(.*?)\]')
        like_count = response.xpath('//a[contains(., "赞[")]//text()').re_first('赞\[(.*?)\]')
        posted_time = response.xpath('//div[@id="M_"]//span[@class="ct"]//text()').extract_first(default=None)
        user = response.xpath('//div[@id="M_"]/div[1]/a/text()').extract_first()
        print(url, id, content, comment_count, forward_count, like_count, posted_time, user, sep='\n')
        weibo_item = WeiboItem()
        for field in weibo_item.fields:
            try:
                weibo_item[field] = eval(field)
            except NameError:
                print('Field(%s) is not defined' % field)
        yield weibo_item
