from selenium import webdriver
import time

u = input('Please input your name:\n')
p = input('Please input your password:\n')

url = 'https://yun.baidu.com/'

driver = webdriver.Chrome()
driver.get(url)

c = driver.find_element_by_class_name('account-title')
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
