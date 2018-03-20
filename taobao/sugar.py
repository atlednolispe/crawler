import pymongo
import re
import time

from lxml import etree
from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from atlednolispe_mongodb import (
    MONGO_URL, MONGO_DB, MONGO_TABLE, KEYWORD
)

# headless Chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=chrome_options)

wait = WebDriverWait(driver, 10)

# connet to MongoDB
client = pymongo.MongoClient(MONGO_URL, connect=False)
db = client[MONGO_DB]


def index():
    """
    访问淘宝首页,进行关键字搜索
    """
    driver.get('https://www.taobao.com')

    try:
        search_box = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#q"))
        )
        search_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_TSearchForm > div.search-button > button"))
        )

        search_box.send_keys(KEYWORD)
        search_button.click()

        total_page = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.total"))
        )
        parse_products()
        return total_page.text
    except TimeoutException:
        return 'So sad!!! TimeoutException.'


def jump_to_page(page_num):
    """
    对淘宝页面进行跳转,爬取所有商品信息
    """
    try:
        search_box = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input"))
        )
        search_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit"))
        )
        search_box.clear()
        search_box.send_keys(page_num)
        search_button.click()
        wait.until(
            EC.text_to_be_present_in_element(
                (
                    By.CSS_SELECTOR,
                    "#mainsrp-pager > div > div > div > ul > li.item.active > span",
                ),
                str(page_num)
            )
        )
        parse_products()
    except TimeoutException:
        jump_to_page(page_num)


def parse_products():
    """
    解析搜索出来的淘宝商品信息


    pyquery使用遇到BUG: 使用list调用PyQuery后原先的PyQuery生成器对象无法迭代

    xpath使用如下方法会无法匹配到正确内容,原因已经解决方案暂时还没有:

    items = html.xpath('//*[@id="mainsrp-itemlist"]//div[@class="items"]//div[contains(@class, "item")]')

    'price': item.xpath('.//div[contains(@class, "price")]//strong/text()'),
    'deal': item.xpath('.//div[class="deal-cnt"]'),
    'location': item.xpath('.//*[class="location"]/text()'),
    'title': item.xpath('.//*[contains(@class, "title")]/text()'),
    'image': item.xpath('.//img/@src')
    """
    try:
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-itemlist .items"))
        )
        html = driver.page_source

        # 解析方案一: pyquery
        # doc = pq(html)
        # items = doc('#mainsrp-itemlist .items .item').items()
        # # print(len(list(items)))  # list之后不能在后面的for循环中迭代items,bug?
        #
        # for item in items:
        #     product = {
        #         'price': item.find('.price').text(),
        #         'deal': item.find('.deal-cnt').text()[:-3],
        #         'shop': item.find('.shop').text(),
        #         'location': item.find('.location').text(),
        #         'title': item.find('.title').text(),
        #         'image': item.find('.pic .img').attr('src'),
        #     }
        #     print(product)

        # 解析方案二: xpath
        html = etree.HTML(html)
        items = html.xpath('//*[@id="mainsrp-itemlist"]/div/div/div[1]/div[*]|//*[@id="J_itemlistPersonality"]/div/div[*]')
        for item in items:
            product = {
                'price': item.xpath('./div[2]/div[1]/div[1]/strong/text()')[0],
                'deal': item.xpath('./div[2]/div[1]/div[2]/text()')[0][:-3],
                'shop': item.xpath('./div[2]/div[3]/div[1]/a/span[2]/text()')[0],
                'location': item.xpath('./div[2]/div[3]/div[2]/text()')[0],
                'title': ''.join([str.strip() for str in item.xpath('.//*[starts-with(@id, "J_Itemlist_TLink")]//text()')]),
                'image': item.xpath('.//*[starts-with(@id, "J_Itemlist_Pic")]/@src')[0],
            }
            save_to_mongodb(product)

    except TimeoutException:
        pass


def save_to_mongodb(data):
    """
    将商品数据存储到MongoDB中
    """
    if db[MONGO_TABLE].insert(data):
        print('Successfully save to MongoDB!')
        return True
    else:
        return False


def main():
    try:
        total_page = index()
        total_page = re.compile('(\d+)').search(total_page).group(1)
        total_page = int(total_page)
        for page_num in range(2, total_page+1):
            print('正在爬取第{}页:\n'.format(page_num))
            jump_to_page(page_num)
    except Exception as e:
        print(e)
    finally:
        driver.quit()


if __name__ == '__main__':
    main()
