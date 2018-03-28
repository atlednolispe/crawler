from selenium import webdriver
import time

u = input('Please input your name:\n')
p = input('Please input your password:\n')

url = 'https://yun.baidu.com/'

driver = webdriver.Chrome()
driver.get(url)

time.sleep(3)
c = driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_4__footerULoginBtn"]')
c.click()

time.sleep(3)

username = driver.find_element_by_class_name('pass-text-input-userName')
username.clear()
username.send_keys(u)

password = driver.find_element_by_class_name('pass-text-input-password')
password.click()
password.clear()
password.send_keys(p)

submit = driver.find_element_by_class_name('pass-button-submit')
submit.click()

time.sleep(10)

cookies = {}
for item in driver.get_cookies():
    cookies[item['name']] = item['value']

print(cookies)
