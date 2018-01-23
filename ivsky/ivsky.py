import urllib
from lxml import etree
import requests


def schedule(blocknum, blocksize, totalsize):
    per = 100 * blocknum * blocksize / totalsize
    if per > 100:
        per = 100
    print('当前下载进度: %d%%' % per, end='')
    if per < 100:
        print('\r', end='')


r = requests.get('http://www.ivsky.com/tupian/ziranfengguang/')
html = etree.HTML(r.text)
img_urls = html.xpath('.//img/@src')

i = 1
for img_url in img_urls:
    urllib.request.urlretrieve(img_url, 'img'+str(i)+'.jpg', schedule)
    i += 1
    print()
