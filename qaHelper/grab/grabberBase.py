# -*- coding: utf-8 -*-

class GrabberBase(object):
    def __init__(self, headers=None, proxy=False):
        if proxy:
            self.proxies = {"http": "socks5://127.0.0.1:1080", 'https': 'socks5://127.0.0.1:1080'}
        else:
            self.proxies = {}
        self.proxy = proxy
        if headers is None:
            self.headers =None
        else:
            self.headers =headers


    def get(self):
        pass

