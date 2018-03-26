from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from atlednolispe_weibo import USER, PASSWORD


driver = webdriver.Chrome()
driver.delete_all_cookies()
url = 'http://my.sina.com.cn/profile/unlogin/'
driver.get(url)

wait = WebDriverWait(driver, 10)


try:
    login_button = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="hd_login"]'))
    )
    login_button.click()

    user = wait.until(
        # presence_of_element_located is not enough
        EC.visibility_of_element_located((By.XPATH, '/html/body/div[6]/div[2]/ul/li[2]/input'))
    )
    password = driver.find_element_by_xpath('/html/body/div[6]/div[2]/ul/li[3]/input')

    login = driver.find_element_by_xpath('/html/body/div[6]/div[2]/ul/li[6]/span/a')

    user.send_keys(USER)
    password.send_keys(PASSWORD)
    login.click()

    my_news = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="l_menu_tt_0"]'))
    )

    if my_news:
        print('Success login!')
        driver.get('https://weibo.cn/')

        if "我的首页" in driver.title:
            cookies = {}
            for item in driver.get_cookies():
                cookies[item['name']] = item['value']

            print(cookies)

except TimeoutException:
    print('Time out!')
