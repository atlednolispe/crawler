import pickle
import hashlib
from baidubaike_distributed.crawler_exception import NoURL


class URLManager:
    def __init__(self):
        self.new_urls = self.load_progress('new_urls.txt')
        self.old_urls = self.load_progress('old_urls.txt')

    def has_new_url(self):
        return self.new_url_size() > 0

    def get_new_url(self):
        new_url = self.new_urls.pop()
        url_md5 = self.url_to_md5(new_url)
        self.old_urls.add(url_md5)
        return new_url

    def add_new_url(self, url):
        if url is None:
            raise NoURL
        url_md5 = self.url_to_md5(url)
        if url not in self.new_urls and url_md5 not in self.old_urls:
            self.new_urls.add(url)

    def add_new_urls(self, urls):
        if urls is None or len(urls) == 0:
            raise NoURL
        for url in urls:
            self.add_new_url(url)

    def new_url_size(self):
        return len(self.new_urls)

    def old_url_size(self):
        return len(self.old_urls)

    def url_to_md5(self, url):
        m = hashlib.md5()
        m.update(url.encode('utf-8'))
        return m.hexdigest()[8:-8]

    def save_progress(self, path, data):
        with open(path, 'wb') as f:
            pickle.dump(data, f)

    def load_progress(self, path):
        print('[+] load from file: %s' % path)
        try:
            with open(path, 'rb') as f:
                tmp = pickle.load(f)
                return tmp
        except Exception:
            print('[!] no progress, create: %s' % path)
        return set()