from baidubaike.crawler_exception import NoData

class DataOutput:
    def __init__(self):
        self.datas = []

    def store_data(self, data):
        if data is None:
            raise NoData
        self.datas.append(data)

    def output_html(self):
        with open('baike.html', 'w') as f:
            f.write("<html>")
            f.write("<head><meta charset='utf-8'/></head>")
            f.write("<body>")
            f.write("<table>")
            for data in self.datas:
                f.write("<tr>")
                f.write("<td>%s</td>" % data['url'])
                f.write("<td>%s</td>" % data['title'])
                f.write("<td>%s</td>" % data['summary'])
                f.write("</tr>")
            f.write("</table>")
            f.write("</body>")
            f.write("</html>")