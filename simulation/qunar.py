from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import re

to_city = '上海'
from_data = '2018-02-03'
to_data = '2018-02-04'


class Qunar:
    def __init__(self, to_city, from_data, to_data):
        self.to_city = to_city
        self.from_data = from_data
        self.to_data = to_data
        self.addr_pattern = re.compile('</b>(.*?)</em>')

    def hotel_of_city(self):
        driver = webdriver.Firefox()
        driver.get('http://hotel.qunar.com/')

        ele_toCity = driver.find_element_by_name('toCity')
        ele_fromDate = driver.find_element_by_id('fromDate')
        ele_toDate = driver.find_element_by_id('toDate')
        ele_search = driver.find_element_by_class_name('search-btn')
        ele_toCity.clear()
        ele_toCity.send_keys(self.to_city)
        ele_fromDate.clear()
        ele_fromDate.send_keys(self.from_data)
        ele_toDate.clear()
        ele_toDate.send_keys(self.to_data)
        ele_search.click()

        return driver

    def crawler(self):
        driver = self.hotel_of_city()
        try:
            WebDriverWait(driver, 10).until(EC.title_contains(to_city))
        except Exception as e:
            print(e)

        first_title_prev = None

        i = 0
        while i < 5:
            time.sleep(2)

            # roll to the bottom of the page
            js = 'window.scrollTo(0,document.body.scrollHeight);'
            driver.execute_script(js)

            time.sleep(5)

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            hotels = soup.find_all(class_='item_hotel_info')
            next = WebDriverWait(driver, 10).until(EC.visibility_of(driver.find_element_by_css_selector('.item.next')))

            first_title = title = hotels[0].find_all('a', class_='e_title js_list_name')[0].string
            # verification of a new page
            if first_title == first_title_prev:
                next.click()
                continue

            first_title_prev = first_title

            i += 1
            print('-' * 10 + str(i) + '-' * 10)

            for hotel in hotels:
                """
                上海玩具总动员酒店
                [<em class="sort dangci" title="去哪儿网用户评定为高档型酒店">高档型</em>, <em><b>，</b>浦东新区申迪西路360号</em>]
                [<b>，</b>, <b>wifi</b>, <b>停车场</b>, <b>4.7</b>, <b>wifi</b>, <b>停车场</b>, <b>1470</b>]
                """
                title = hotel.find_all('a', class_='e_title js_list_name')[0].string
                try:
                    address = self.addr_pattern.findall(str(hotel.find_all('em')[1]))[0]
                except Exception as e:
                    address = hotel.find_all('em')[1].string
                price = hotel.find_all('b')[-1].string
                while price is None:
                    time.sleep(1)
                    price = hotel.find_all('b')[-1].string

                print(title)
                print(address)
                print(price)

            next.click()


i = Qunar(to_city, from_data, to_data)
i.crawler()
