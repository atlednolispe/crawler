import requests
from baidubaike.crawler_exception import URLStateError


class HTMLDownloader:
    def download(self, url):
        user_agent = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/63.0.3239.132 Safari/537.36')
        headers = {'user-agent': user_agent}
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            r.encoding = 'utf-8'
            return r.text
        raise URLStateError
