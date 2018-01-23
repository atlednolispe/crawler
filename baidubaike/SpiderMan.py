from baidubaike.URLManager import URLManager
from baidubaike.HTMLDownloader import HTMLDownloader
from baidubaike.HTMLParser import HTMLParser
from baidubaike.DataOutput import DataOutput


class SpiderMan:
    def __init__(self):
        self.manager = URLManager()
        self.downloader = HTMLDownloader()
        self.parser = HTMLParser()
        self.output = DataOutput()

    def crawl(self, root_url):
        self.manager.add_new_url(root_url)
        while self.manager.has_new_url() and self.manager.old_url_size() < 10:
            try:
                new_url = self.manager.get_new_url()
                html = self.downloader.download(new_url)
                new_urls, data = self.parser.parser(new_url, html)
                self.manager.add_new_urls(new_urls)
                self.output.store_data(data)
                print('%s links had been saved!' % self.manager.old_url_size())
            except Exception as e:
                print(e)
        self.output.output_html()


if __name__ == "__main__":
    # add PYTHONPATH or python -m
    spider_man = SpiderMan()
    spider_man.crawl("http://baike.baidu.com/view/284853.htm")
