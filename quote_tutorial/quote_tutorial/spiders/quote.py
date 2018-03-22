# -*- coding: utf-8 -*-
import scrapy

from ..items import QuoteTutorialItem


class QuoteSpider(scrapy.Spider):
    name = 'quote'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes = response.css('.quote')
        for quote in quotes:
            text = quote.css('.text::text').extract_first()
            author = quote.css('.author::text').extract_first()
            tags = quote.css('.tags .tag::text').extract()

            item = QuoteTutorialItem()
            item['text'] = text
            item['author'] = author
            item['tags'] = tags
            yield item

        next_page_url_extracted = response.css('.pager .next a::attr(href)').extract_first()
        next_page_url = response.urljoin(next_page_url_extracted)
        yield scrapy.Request(url=next_page_url, callback=self.parse)