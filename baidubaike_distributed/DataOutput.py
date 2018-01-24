from baidubaike_distributed.crawler_exception import NoData
import time


class DataOutput:
    def __init__(self):
        now = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        self.filepath = 'baike_%s.html' % now
        self.output_head()
        self.datas = []

    def store_data(self, data):
        if data is None:
            raise NoData
        self.datas.append(data)
        if len(self.datas) > 10:
            self.output_html()

    def output_head(self):
        with open(self.filepath, 'w') as f:
            f.write("<html>")
            f.write("<head><meta charset='utf-8'/></head>")
            f.write("<body>")
            f.write("<table>")

    def output_html(self):
        with open(self.filepath, 'a') as f:
            for data in self.datas:
                f.write("<tr>")
                f.write("<td>%s</td>" % data['url'])
                f.write("<td>%s</td>" % data['title'])
                f.write("<td>%s</td>" % data['summary'])
                f.write("</tr>")
            self.datas = []

    def output_tail(self):
        with open(self.filepath, 'a') as f:
            f.write("</table>")
            f.write("</body>")
            f.write("</html>")
