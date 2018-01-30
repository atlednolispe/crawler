import requests

# copy request headers from chrome
headers_baiduyun = """
Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Encoding:gzip, deflate, br
Accept-Language:zh-CN,zh;q=0.9
Connection:keep-alive
Cookie:*
Host:yun.baidu.com
Upgrade-Insecure-Requests:1
User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36
"""

headers = {}
cookies = {}

for line in headers_baiduyun.strip().split('\n'):
    k, v = line.split(':', 1)
    if k != 'Cookie':
        headers[k] = v
    else:
        for couple in v.split('; '):
            k1, v1 = couple.split('=', 1)
            cookies[k1] = v1
print(headers)
print(cookies)

url = 'https://yun.baidu.com/'
r = requests.get(url, headers=headers, cookies=cookies)
r.encoding = 'utf-8'
print(r.status_code)
print(r.text)