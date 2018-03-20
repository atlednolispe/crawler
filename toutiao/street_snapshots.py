import json
import os
import pymongo
import re
import requests

from bs4 import BeautifulSoup
from hashlib import md5
from multiprocessing import Pool
from requests.exceptions import RequestException

from atlednolispe_mongodb import (
    MONGO_URL, MONGO_DB, MONGO_TABLE, START_INDEX, END_INDEX, KEYWORD,
)


HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) ' 
                  'Chrome/65.0.3325.162 Safari/537.36',
}

URL = 'https://www.toutiao.com/search_content/'

data = {
    'offset': '0',
    'format': 'json',
    'keyword': KEYWORD,
    'autoload': 'true',
    'count': '20',
    'cur_tab': '3',
    'from': 'gallery',
}

# connet to MongoDB
client = pymongo.MongoClient(MONGO_URL, connect=False)
db = client[MONGO_DB]


def get_image_set_json_str(query_data):
    """
    获取头条搜索的图集json数据
    """
    try:
        response = requests.get(URL, params=query_data)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('获取图集详细json数据({url})失败'.format(url=URL))
        return None


def parse_url_list(json_str):
    """
    解析图集json中的所有url
    """
    data = json.loads(json_str)
    if data and 'data' in data:
        for item in data.get('data'):
            yield item.get('article_url')


def get_image_html(url):
    """
    获取每个图集链接的详情html内容
    """
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('获取{url}图集html失败'.format(url=url))
        return None


def parse_image(html, url):
    """
    解析图集名和图集中的所有图片的url
    """
    soup = BeautifulSoup(html, 'lxml')
    title = soup.head.title.string

    pattern = re.compile('JSON.parse\("(.*?)"\),')
    result = re.search(pattern, html)
    if result:
        clean_result = result.group(1).replace('\\', '')
        data = json.loads(clean_result)
        if data and 'sub_images' in data:
            sub_images = data.get('sub_images')
            images = [item['url'] for item in sub_images]
            return {
                'title': title,
                'url': url,
                'images': images,
            }
        else:
            print('error parse image')


def save_to_mongodb(data):
    """
    将图集数据存储到MongoDB中
    """
    if db[MONGO_TABLE].insert(data):
        print('Successfully save {url} to MongoDB!'.format(url=data['url']))
        return True
    else:
        return False


def download_image(url):
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            print('正在下载', url)
            return save_image(response.content)
        return None
    except RequestException:
        print('获取图片({url})失败'.format(url=url))
        return None


def save_image(content):
    """
    保存图片前先通过md5检验防止图片的重复下载
    """
    file_path = '{dir}/{file_name}.{suffix}'.format(
        dir=os.getcwd(),
        file_name=md5(content),
        suffix='jpg'
    )
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()


def street_snapshots(offset):
    query = data
    query['offset'] = str(offset)
    json_str = get_image_set_json_str(query)

    for url in parse_url_list(json_str):
        html = get_image_html(url)
        if html:
            result = parse_image(html, url)
            if result:
                save_to_mongodb(result)
            # for image in result['images']:
            #     download_image(image)


def main():
    pool = Pool()
    pool.map(street_snapshots, (i*20 for i in range(START_INDEX, END_INDEX+1)))


if __name__ == '__main__':
    main()
