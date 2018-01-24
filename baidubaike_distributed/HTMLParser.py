import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from baidubaike_distributed.crawler_exception import NoURL, NoHTML


class HTMLParser:
    def parser(self, page_url, html_content):
        if page_url is None:
            raise NoURL
        if html_content is None:
            raise NoHTML

        soup = BeautifulSoup(html_content, 'html.parser')
        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data

    def _get_new_urls(self, page_url, soup):
        new_urls = set()
        links = soup.find_all('a', href=re.compile(r'/(view|item)/.*'))
        for link in links:
            new_url = link['href']
            new_full_url = urljoin(page_url, new_url)
            new_urls.add(new_full_url)
        return new_urls

    def _get_new_data(self, page_url, soup):
        data = dict()
        data['url'] = page_url
        title = soup.find('dd', class_="lemmaWgt-lemmaTitle-title").find('h1')
        data['title'] = title.get_text()
        summary = soup.find('div', attrs={"class": "para", "label-module": "para"})
        data['summary'] = summary.get_text()
        return data
