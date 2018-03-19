import json
from multiprocessing import Pool
import re
import requests

from requests.exceptions import RequestException


HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) ' 
                  'Chrome/65.0.3325.162 Safari/537.36',
}

URL = 'https://maoyan.com/board/4'


def get_single_html(offset):
    try:
        response = requests.get(URL, params={'offset': offset}, headers=HEADERS)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except RequestException:
        return None


def parse_html(html):
    pattern = re.compile('<dd>.*?class="board-index.*?">(\d*?)<.*?data-src="(.*?)".*?<p class="name">.*?<a href="(.*?)"'
                         ' title="(.*?)".*?</p>.*?<p class="star">(.*?)</p>.*?<p class="releasetime">(.*?)</p>.*?'
                         'class="integer">(.*?)<.*?class="fraction">(.*?)<.*?</dd>',
                         re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'img': item[1],
            'url': 'https://maoyan.com' + item[2],
            'title': item[3],
            'actors': item[4].strip()[3:],
            'release_time': item[5].split('(')[0][5:],
            'release_region': item[5].split('(')[-1][:-1],
            'score': item[6] + item[7]
        }


def save_to_file(info):
    with open('data_maoyan_top100.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(info, ensure_ascii=False) + '\n')


def crawler(offset):
    html = get_single_html(offset)
    for item in parse_html(html):
        save_to_file(item)


def main():
    pool = Pool()
    pool.map(crawler, (i*10 for i in range(10)))


if __name__ == '__main__':
    main()
