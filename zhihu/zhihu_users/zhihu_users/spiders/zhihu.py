# -*- coding: utf-8 -*-
import json
import scrapy

from scrapy import Request

from ..items import ZhihuUsersItem


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    followees_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    followers_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}'

    start_user = 'excited-vczh'

    user_query = 'locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,answer_count,articles_count,pins_count,question_count,commercial_question_count,favorite_count,favorited_count,logs_count,marked_answers_count,marked_answers_text,message_thread_token,account_status,is_active,is_force_renamed,is_bind_sina,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics'
    followees_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'
    followers_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    def start_requests(self):
        yield Request(
            self.user_url.format(user=self.start_user, include=self.user_query),
            self.parse_user
        )
        yield Request(
            self.followees_url.format(user=self.start_user, include=self.followees_query, limit=20, offset=0),
            self.parse_followees
        )
        yield Request(
            self.followers_url.format(user=self.start_user, include=self.followers_query, limit=20, offset=0),
            self.parse_followers
        )

    def parse_user(self, response):
        result = json.loads(response.text)
        item = ZhihuUsersItem()

        for field in item.fields:
            if field in result:
                item[field] = result.get(field)
        yield item

        yield Request(
            self.followees_url.format(user=result.get('url_token'), include=self.followees_query, limit=20, offset=0),
            self.parse_followees)

        yield Request(
            self.followers_url.format(user=result.get('url_token'), include=self.followers_query, limit=20, offset=0),
            self.parse_followers)

    def parse_followees(self, response):
        results = json.loads(response.text)

        if 'data' in results:
            for result in results.get('data'):
                yield Request(
                    self.user_url.format(user=result.get('url_token'), include=self.user_query),
                    self.parse_user
                )

        if 'paging' in results and results.get('paging').get('is_end') is False:
            next_page = results.get('paging').get('next')
            yield Request(
                next_page,
                self.parse_followees
            )

    def parse_followers(self, response):
        results = json.loads(response.text)

        if 'data' in results:
            for result in results.get('data'):
                yield Request(
                    self.user_url.format(user=result.get('url_token'), include=self.user_query),
                    self.parse_user
                )

        if 'paging' in results and results.get('paging').get('is_end') is False:
            next_page = results.get('paging').get('next')
            yield Request(
                next_page,
                self.parse_followers
            )
