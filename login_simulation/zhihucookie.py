import requests

# delete Accept-Encoding:gzip, deflate, copy from chrome request headers
headers_zhihu = """
Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Language:zh-CN,zh;q=0.9
Connection:keep-alive
Cookie:*
Host:www.zhihu.com
Upgrade-Insecure-Requests:1
User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36
"""

headers = {}
cookies = {}

for line in headers_zhihu.strip().split('\n'):
    k, v = line.split(':', 1)
    if k != 'Cookie':
        headers[k] = v
    else:
        for couple in v.split('; '):
            k1, v1 = couple.split('=', 1)
            cookies[k1] = v1
print(headers)
print(cookies)

url = 'https://www.zhihu.com/'
r = requests.get(url, headers=headers, cookies=cookies)
print(r.status_code)
print(r.text)