import hashlib
import hmac
import pickle
import time

import requests.utils


"""
请求头: 仅添加User-Agent即可,在之后的模拟登录中还需加入authorization和X-Xsrftoken
"""
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:60.0) Gecko/20100101 Firefox/60.0',
}

ZHIHU_URL = 'https://www.zhihu.com/{suffix}'
SIGN_UP = 'signup?next=%2F'
CAPTCHA_API = 'api/v3/oauth/captcha?lang={mode}'
SIGN_IN_API = 'api/v3/oauth/sign_in'
ZAP_URL = 'https://unpkg.zhimg.com/za-js-sdk@latest/dist/zap.js'

CLIENT_ID = 'c3cef7c66a1843f8b3a9e6a1e3160e20'
GRANT_TYPE = 'password'
SOURCE = 'com.zhihu.web'
OAUTH = 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20'

"""
用于登录POST请求的参数
"""
PAYLOAD = {
    'client_id': CLIENT_ID,
    'grant_type': GRANT_TYPE,
    'timestamp': '',
    'source': SOURCE,
    'signature': '',
    'username': '',
    'password': '',
    'captcha': '',
    'lang': 'cn',
    'ref_source': 'homepage',
    'utm_source': '',
}


class ZhihuLogin:
    def __init__(self):
        self.headers = HEADERS
        self.session = requests.session()
        self.session.headers = self.headers
        self.homepage_url = ZHIHU_URL.format(suffix='')
        self.captcha_url = ZHIHU_URL.format(suffix=CAPTCHA_API)
        self.signin_url = ZHIHU_URL.format(suffix=SIGN_IN_API)
        self.payload = PAYLOAD

    def login(self, username=None, password=None, cookies_path=None):
        if cookies_path:
            self._load_cookies(cookies_path)
        else:
            username, password = self._check_username_and_password(username, password)
            self._login_simulation(username, password)

        success_login = self._check_login()
        self._dump_cookies()
        if success_login:
            return True
        else:
            return False

    def _login_simulation(self, username, password):
        """
        知乎的模拟登录中涉及多次请求,并且存在多次response的set-cookie行为。
        选择利用requests的session实现模拟登录。

        1. 请求知乎首页 https://www.zhihu.com/
        302到注册页面 https://www.zhihu.com/signup?next=/
        会set-cookie: X-Xsrftoken

        2. 请求验证码接口 https://www.zhihu.com/api/v3/oauth/captcha?lang=en (或lang=cn)
        set-cookie: capsion_ticket

        3. 使用加密后的参数POST请求登录api接口 https://www.zhihu.com/api/v3/oauth/sign_in
        """
        self.payload['username'] = username
        self.payload['password'] = password
        r1 = self.session.get(self.homepage_url)
        xsrftoken = self.session.cookies.get('_xsrf')
        self._skip_captcha()
        self.session.headers.update({'X-Xsrftoken': xsrftoken})
        timestamp = str(int(time.time()*1000))
        self.payload['timestamp'] = timestamp
        self._get_signature()
        r3 = self.session.post(self.signin_url, data=self.payload)

        # 成功获取cookies后的登录不需要在请求头中添加以下内容
        self.session.headers.pop('authorization')
        self.session.headers.pop('X-Xsrftoken')

    def _get_signature(self):
        """
        登录的POST请求中的signature参数需要hamc加密,此方法引用自知乎用户口可口可,
        链接: https://zhuanlan.zhihu.com/p/34073256

        grant_type和client_id都是写死在js中的内容。

        加密是使用的都是bytes不是str。
        """
        key = b"d1b964811afb40118a12068ff74a12f4"
        hamc_object = hmac.new(key, digestmod=hashlib.sha1)
        hamc_object.update(self.payload['grant_type'].encode())
        hamc_object.update(self.payload['client_id'].encode())
        hamc_object.update(self.payload['source'].encode())
        hamc_object.update(self.payload['timestamp'].encode())
        signature = hamc_object.hexdigest()
        self.payload['signature'] = signature
        return signature

    def _skip_captcha(self):
        """
        如果遇到需要验证码的情况,再次请求验证码api接口,用于跳过验证码。
        """
        self.session.headers.update({'authorization': OAUTH})
        captcha_url = self.captcha_url.format(mode='en')
        r2 = self.session.get(captcha_url)
        while 'true' in r2.text:
            r2 = self.session.get(captcha_url)

    def _check_username_and_password(self, username, password):
        if not username:
            username = input('请输入手机号: ')
        if not password:
            password = input('请输入密码: ')
        if not username.startswith('+86'):
            username = '+86' + username  # 直接使用手机号开头不添加+86也可以
        return username, password

    def _load_cookies(self, cookies_path):
        with open(cookies_path, 'rb') as f:
            cookies = requests.utils.cookiejar_from_dict(pickle.load(f))
            self.session.cookies = cookies

    def _dump_cookies(self, cookies_path=None):
        if not cookies_path:
            cookies_path = '{username}_cookies.pickle'.format(username=self.payload['username'][3:])
        with open(cookies_path, 'wb') as f:
            pickle.dump(requests.utils.dict_from_cookiejar(self.session.cookies), f)

    def _check_login(self):
        response = self.session.get(self.homepage_url)
        if '首页 - 知乎' in response.text:
            print('登录成功')
            return True
        else:
            print('登录失败')
            return False


if __name__ == '__main__':
    user1 = ZhihuLogin()
    user1.login()
