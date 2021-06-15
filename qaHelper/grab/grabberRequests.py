# -*- coding: utf-8 -*-
"""
requests using proxy
import requests
headers = {'user-agent': ''}
proxies = {"http": "socks5://127.0.0.1:1080",'https': 'socks5://127.0.0.1:1080'}
proxies = {"http": "socks5h://127.0.0.1:1080",'https': 'socks5h://127.0.0.1:1080'}  # for ipv6


# url = 'https://www.baidu.com/'
url = 'https://www.google.com/search?q=python' #
res = requests.get(url, headers=headers, proxies=proxies)
print("res.status_code:\n",res.status_code)

url = 'http://icanhazip.com' # my ip
res = requests.get(url, headers=headers, proxies=proxies)
print("res.status_code:\n",res.status_code)
print(res.text)

"""
import requests
import random
from .grabberBase import GrabberBase


def get_UA():
    """随机返回user agent

    Returns:

    """
    uastrings = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36",
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
        ]

    return random.choice(uastrings)

class GrabberRequests(GrabberBase):
    def __init__(self, headers=None, proxy=False):
        super().__init__(headers,proxy)

    def get(self, url="", params={}):
        """

        Args:
            url:
            params:

        Returns:

        """
        headers = {'User-Agent': get_UA()}
        headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
        headers['Accept-Language']= "en, zh-CN;q = 0.9, zh;q = 0.8, en-AU;q = 0.7, zh-TW;q = 0.6"
        return requests.get(url=url, headers=headers, proxies=self.proxies, params=params)
        # return requests.get(url=url, headers=headers,params=params)

    def post(self, url="", params={}):
        pass
