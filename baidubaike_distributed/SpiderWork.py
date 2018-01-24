from multiprocessing.managers import BaseManager
from baidubaike_distributed.HTMLDownloader import HTMLDownloader
from baidubaike_distributed.HTMLParser import HTMLParser


class SpiderWork:
    def __init__(self):
        BaseManager.register('get_task_queue')
        BaseManager.register('get_result_queue')

        server_addr = '192.168.3.3'
        print('connet to server %s' % server_addr)

        self.m = BaseManager(address=(server_addr, 7777), authkey='baike'.encode('utf-8'))
        self.m.connect()
        self.task = self.m.get_task_queue()
        self.result = self.m.get_result_queue()
        self.downloader = HTMLDownloader()
        self.parser = HTMLParser()

        print('spider init finish')

    def crawl(self):
        while True:
            try:
                if not self.task.empty():
                    url = self.task.get()

                    if url == 'end':
                        print('控制节点通知爬虫节点停止工作')
                        self.result.put({'new_urls': 'end', 'data': 'end'})
                        return
                    print('爬虫节点正在解析: %s' % url)
                    content = self.downloader.download(url)
                    new_urls, data = self.parser.parser(url, content)
                    self.result.put({'new_urls': new_urls, 'data': data})
            except EOFError:
                print('连接工作节点失败')
            except Exception as e:
                print(e)
                print('crawl fail')


if __name__ == '__main__':
    spider = SpiderWork()
    spider.crawl()