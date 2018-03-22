import json
import pymongo
import requests
import time

from lxml import etree
from requests.exceptions import RequestException

from atlednolispe_wechat import (
    HEADERS as HEADERS_CONFIG, MONGO_URL, MONGO_DB, MONGO_TABLE, KEYWORD
)

MAX_REQUESTS = 5

BASE_URL = 'http://weixin.sogou.com/weixin'
PROXY_POOL_URL = 'http://127.0.0.1:5000/get'
# PROXY_POOL_URL = 'http://192.168.50.111:8000?type=0&count=10'

QUERY = {
    'query': KEYWORD,
    'type': 2,
    'page': 20,
    'ie': 'utf8',
}

HEADERS = {}
for item in HEADERS_CONFIG.strip().split('\n'):
    k,v = item.split(': ')
    HEADERS[k] = v


# connet to MongoDB
client = pymongo.MongoClient(MONGO_URL, connect=False)
db = client[MONGO_DB]


def haipproxy_or_not():
    import sys
    sys.path.append(HAIPPROXY_PATH)

    from client.py_cli import ProxyFetcher

    return True


def get_list(query, count=1, proxy=None):
    """
    crwaler change proxy per num pages.
    """
    if count > MAX_REQUESTS:
        print('request bigger than 5')
        return None
    try:
        proxies = {
            'http': 'http://' + proxy,
            # 'http': PROXY,  # haipproxy
        }
        response = requests.get(BASE_URL, params=query, allow_redirects=False, headers=HEADERS, proxies=proxies)
        if response.status_code == 200:
            return response.content.decode('utf-8')  # response.text sometime can't be readable
        elif response.status_code == 302:
            # proxy
            print('302')
            new_proxy = get_proxy()
            if new_proxy:
                print('Using Proxy', new_proxy)
                return get_list(query, count, proxy=new_proxy)  # change proxy don't add count
            else:
                print('Get Proxy Failed')
                time.sleep(60)
                new_proxy = get_proxy()
                if not new_proxy:
                    return None
                else:
                    return get_list(query, count, proxy=new_proxy)
    except RequestException:
        new_proxy = get_proxy()
        return get_list(query, count+1, proxy=new_proxy)


def get_proxy_list():  # haipproxy
    args = dict(host='127.0.0.1', port=6379, password=None, db=0)
    fetcher = ProxyFetcher('zhihu', strategy='greedy', redis_args=args)
    return fetcher.get_proxies()


# PROXIES = get_proxy_list()  # haipproxy

proxy_num = 0


def get_proxy():
    global proxy_num
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
        return None

        # if PROXIES:
        #     return PROXIES.pop()

        # r = requests.get(PROXY_POOL_URL)
        # ip = json.loads(r.text)
        # proxy_num += 1
        # return ip[proxy_num][0] + ":" + str(ip[proxy_num][1])

    except RequestException:
        return None


def parse_url_list(html):
    html = etree.HTML(html)
    items = html.xpath('//*[starts-with(@id, "sogou_vr_11002601_box")]//*[starts-with(@id, "sogou_vr_11002601_title")]/@href')
    for item in items:
        yield item


def get_article_html(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_article(html):
    try:
        html = etree.HTML(html)
        title = html.xpath('//*[@id="activity-name"]/text()')[0].strip()
        content = '\n'.join(p.strip() for p in html.xpath('//*[@id="js_content"]//p//text()'))
        date = html.xpath('//*[@id="post-date"]/text()')[0]
        author = html.xpath('//*[@id="post-user"]/text()')[0]
        return {
            'title': title,
            'content': content,
            'date': date,
            'author': author,
        }
    except Exception as e:
        print(e.args)


def save_to_mongodb(data):
    if db[MONGO_TABLE].update({'title': data['title']}, {'$set': data}, True):
        print('Successfully save {data} to MongoDB!'.format(data=data))
    else:
        print('Save to MongoDB failed! ({})'.format(data))


def main():
    for i in range(1, 101):
        print(i)
        if i % 5 == 0:  # ERROR: i+1 % 10
            proxy = get_proxy()
            if proxy is None:
                time.sleep(60)
                proxy = get_proxy()
                if proxy is None:
                    print('proxy is empty!')
                    break
            print(proxy)
        QUERY['page'] = i
        html = get_list(QUERY, proxy=proxy)
        if html:
            url_list = parse_url_list(html)

            for url in url_list:
                html = get_article_html(url)
                data = parse_article(html)
                if data:
                    save_to_mongodb(data)
        else:
            print('{} parse url_list failed!'.format(QUERY))


if __name__ == '__main__':
    main()
