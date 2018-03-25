# -*- coding: utf-8 -*-

import scrapy


class ZhihuUsersItem(scrapy.Item):
    is_followed = scrapy.Field()
    educations = scrapy.Field()
    following_count = scrapy.Field()

    vote_from_count = scrapy.Field()
    user_type = scrapy.Field()
    show_sina_weibo = scrapy.Field()

    pins_count = scrapy.Field()
    is_following = scrapy.Field()
    marked_answers_text = scrapy.Field()

    account_status = scrapy.Field()
    is_force_renamed = scrapy.Field()
    id = scrapy.Field()

    favorite_count = scrapy.Field()
    voteup_count = scrapy.Field()
    commercial_question_count = scrapy.Field()

    is_blocking = scrapy.Field()
    following_columns_count = scrapy.Field()
    headline = scrapy.Field()

    url_token = scrapy.Field()
    participated_live_count = scrapy.Field()
    following_favlists_count = scrapy.Field()

    is_advertiser = scrapy.Field()
    is_bind_sina = scrapy.Field()
    favorited_count = scrapy.Field()

    is_org = scrapy.Field()
    follower_count = scrapy.Field()
    employments = scrapy.Field()

    type = scrapy.Field()
    avatar_url_template = scrapy.Field()
    following_topic_count = scrapy.Field()

    description = scrapy.Field()
    business = scrapy.Field()
    avatar_url = scrapy.Field()

    hosted_live_count = scrapy.Field()
    is_active = scrapy.Field()
    thank_to_count = scrapy.Field()

    mutual_followees_count = scrapy.Field()
    marked_answers_count = scrapy.Field()
    cover_url = scrapy.Field()

    thank_from_count = scrapy.Field()
    vote_to_count = scrapy.Field()
    is_blocked = scrapy.Field()

    answer_count = scrapy.Field()
    allow_message = scrapy.Field()
    articles_count = scrapy.Field()

    name = scrapy.Field()
    question_count = scrapy.Field()
    locations = scrapy.Field()

    badge = scrapy.Field()
    url = scrapy.Field()
    message_thread_token = scrapy.Field()

    logs_count = scrapy.Field()
    following_question_count = scrapy.Field()
    thanked_count = scrapy.Field()

    gender = scrapy.Field()
