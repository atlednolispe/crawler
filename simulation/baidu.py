from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time

# set path to browser and driver
# binary = FirefoxBinary('/Applications/FirefoxDeveloperEdition.app/Contents/MacOS/firefox')
# driver = webdriver.Firefox(firefox_binary=binary, executable_path='/Users/xxx/Downloads/geckodriver')

driver = webdriver.Chrome()
driver.get("http://www.baidu.com")

assert '百度' in driver.title

elem = driver.find_element_by_name('wd')
elem.clear()
elem.send_keys('crawler')
elem.send_keys(Keys.RETURN)

time.sleep(3)

assert 'crawler' not in driver.page_source

driver.close()