from mtime.downloader import Downloader
from mtime.reponse_parser import ResponseParser
from mtime.data_outputer import DataOutput


class SpiderMan:
    def __init__(self, request_headers, collection):
        self.downloader = Downloader(request_headers)
        self.parser = ResponseParser()
        self.outputer = DataOutput(collection)

    def crawler(self, root_url):
        html = self.downloader.html_download(root_url)
        urls = self.parser.url_parser(html)
        for url in urls:
            raw_json = self.downloader.json_download(url["Id"])
            clean_json = self.parser.json_parser(raw_json)
            self.outputer.store_data(clean_json)
        self.outputer.store_flush()


if __name__ == '__main__':
    request_headers = ("User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/63.0.3239.132 Safari/537.36")
    collection = 'raw_hot_showing'
    spider = SpiderMan(request_headers, collection)
    spider.crawler('http://theater.mtime.com/')
