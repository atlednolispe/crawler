from lxml import etree
import os
import re
import csv

seputu_dir = os.path.dirname(os.path.dirname(__file__))
html_path = os.path.join(seputu_dir, 'save_to_json/seputu.html')

# ValueError: can only parse strings
html = etree.HTML(open(html_path).read())

mulus = html.xpath('.//*[@class="mulu"]')

rows = []
pattern = re.compile(r'\[(.*)\] (.*)')
for mulu in mulus:
    h2 = mulu.xpath('./div[@class="mulu-title"]/center/h2/text()')
    if h2:
        h2_title = h2[0]
        chapter_list = []
        for a in mulu.xpath('./div[@class="box"]/ul/li/a'):
            href = a.xpath('./@href')[0]
            box_title = a.xpath('./@title')[0]
            match = pattern.search(box_title)
            date = match.group(1)
            box_title = match.group(2)
            content = (h2_title, box_title, href, date)
            rows.append(content)

headers = ['title', 'real_title', 'href', 'date']
with open('seputu.csv', 'w') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerows(rows)
