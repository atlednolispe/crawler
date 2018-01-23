import requests
from bs4 import BeautifulSoup
import json

r = requests.get('http://seputu.com')
with open('seputu.html', 'w') as f:
    f.write(r.text)

soup = BeautifulSoup(open('seputu.html'), 'lxml')

content = []

for mulu in soup.find_all(class_='mulu'):
    h2 = mulu.find('h2')
    try:  # 盗墓笔记-南派三叔经典巨作 h2 = None
        h2_title = h2.string
        chapter_list = []
        for a in mulu.find(class_='box').find_all('a'):
            href = a.get('href')
            box_title = a.string
            chapter_list.append({'href': href, 'box_title': box_title})
        content.append({'title': h2_title, 'content': chapter_list})
    except AttributeError:
        pass

with open('seputu.json', 'w') as fp:
    json.dump(content, fp=fp, indent=4, ensure_ascii=False)
