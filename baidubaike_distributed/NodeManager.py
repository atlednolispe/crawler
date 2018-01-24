import time
from multiprocessing.managers import BaseManager
from multiprocessing import Process, Queue
from baidubaike_distributed.URLManager import URLManager
from baidubaike_distributed.DataOutput import DataOutput


class NodeManager:
    def __init__(self, i):
        self.spider_num = i

    def start_manager(self, url_q, result_q):
        BaseManager.register('get_task_queue', callable=lambda: url_q)
        BaseManager.register('get_result_queue', callable=lambda: result_q)

        manager = BaseManager(address=('', 7777), authkey='baike'.encode('utf-8'))
        return manager

    def url_manager_proc(self, url_q, conn_q, root_url):
        url_manager = URLManager()
        url_manager.add_new_url(root_url)

        while True:
            while url_manager.has_new_url():
                new_url = url_manager.get_new_url()
                url_q.put(new_url)
                print('old urls =', url_manager.old_url_size())

                if url_manager.old_url_size() > 2000:
                    for i in range(self.spider_num):
                        url_q.put('end')
                    print('控制节点发起结束通知!')
                    url_manager.save_progress('new_urls.txt', url_manager.new_urls)
                    url_manager.save_progress('old_urls.txt', url_manager.old_urls)
                    return

            try:
                if not conn_q.empty():
                    urls = conn_q.get()  # get a urls list
                    url_manager.add_new_urls(urls)
            except Exception:
                time.sleep(0.1)

    def result_solve_proc(self, result_q, conn_q, store_q):
        while True:
            try:
                if not result_q.empty():
                    content = result_q.get(True)
                    if content['new_urls'] == 'end':
                        print('结果分析进程接收通知然后结束!')
                        store_q.put('end')
                        return
                    conn_q.put(content['new_urls'])
                    store_q.put(content['data'])
                else:
                    time.sleep(0.1)
            except Exception:
                time.sleep(0.1)

    def store_proc(self, store_q):
        output = DataOutput()
        while True:
            if not store_q.empty():
                data = store_q.get()
                if data == 'end':
                    print('存储进程接受通知然后结束!')
                    output.output_tail()
                    return
                output.store_data(data)
            else:
                time.sleep(0.1)


if __name__ == '__main__':
    url_q = Queue()
    result_q = Queue()
    conn_q = Queue()
    store_q = Queue()

    spider_num = 2
    node = NodeManager(spider_num)
    manager = node.start_manager(url_q, result_q)
    root_url = 'http://baike.baidu.com/view/284853.htm'

    url_manager_proc = Process(target=node.url_manager_proc, args=(url_q, conn_q, root_url))
    result_solve_proc = Process(target=node.result_solve_proc, args=(result_q, conn_q, store_q))
    store_proc = Process(target=node.store_proc, args=(store_q,))

    url_manager_proc.start()
    result_solve_proc.start()
    store_proc.start()
    manager.get_server().serve_forever()