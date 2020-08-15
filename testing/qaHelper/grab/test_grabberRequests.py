# -*- coding: utf-8 -*-
"""

"""

import unittest
from unittest import TestCase
# from bs4 import BeautifulSoup
import json
from qaHelper.grab.grabberRequests import GrabberRequests as grequests


class test_GrabberRequests(TestCase):
    def test_get(self):
        """查询巨潮资讯业务预增
        验证两种方式获取数据
            import requests
            url="http://www.cninfo.com.cn/new/fulltextSearch/full?searchkey=%E4%B8%9A%E7%BB%A9%E9%A2%84%E5%A2%9E&sdate=&edate=&isfulltext=false&sortName=pubdate&sortType=desc&pageNum=1"
            res=requests.get(url)
            html=res.text

            pdf路径： http://static.cninfo.com.cn/finalpage/2020-08-04/1208119236.PDF
            Returns:

        """

        gr = grequests()
        url = "http://www.cninfo.com.cn/new/fulltextSearch/full"
        params = {'searchkey': "业绩预增",
                  'sdate': '',
                  'edate': "",
                  # 'isfulltext':'False',
                  'isfulltext': False,  # 不佳引号也可以
                  'sortName': "pubdate",
                  'sortType': "desc",
                  'pageNum': '1'
                  }
        res = grequests.get(url=url, params=params)
        self.assertTrue(res.status_code == 200)
        print(res.content)

        url = "http://www.cninfo.com.cn/new/fulltextSearch/full?searchkey=%E4%B8%9A%E7%BB%A9%E9%A2%84%E5%A2%9E&sdate=&edate=&isfulltext=false&sortName=pubdate&sortType=desc&pageNum=1"
        res2 = grequests.get(url=url)
        self.assertTrue(res.content == res2.content)

    def test_get_json(self):
        """查询巨潮资讯业务预增
            import requests
            url="http://www.cninfo.com.cn/new/fulltextSearch/full?searchkey=%E4%B8%9A%E7%BB%A9%E9%A2%84%E5%A2%9E&sdate=&edate=&isfulltext=false&sortName=pubdate&sortType=desc&pageNum=1"
            res=requests.get(url)
            html=res.text
            Returns:

        """

        gr = grequests()
        url = "http://www.cninfo.com.cn/new/fulltextSearch/full"
        params = {'searchkey': "业绩预增",
                  'sdate': '',
                  'edate': "",
                  # 'isfulltext':'False',
                  'isfulltext': False,  # 不佳引号也可以
                  'sortName': "pubdate",
                  'sortType': "desc",
                  'pageNum': '1'
                  }
        res = grequests.get(url=url, params=params)
        self.assertTrue(res.status_code == 200)
        print(res.content)
        j = json.loads(res.content)
        print("总页数：", j.get("totalpages"))
        print("", j.get('announcements'))
        for item in j.get('announcements'):
            j2 = json.loads(json.dumps(item))
            if len(j2.get('secCode')) == 6:
                print(item)
                for key in j2.keys():
                    print(key)

    def test_get_json_2(self):
        """查询巨潮资讯业务预增
            import requests
            url="http://www.cninfo.com.cn/new/fulltextSearch/full?searchkey=%E4%B8%9A%E7%BB%A9%E9%A2%84%E5%A2%9E&sdate=&edate=&isfulltext=false&sortName=pubdate&sortType=desc&pageNum=1"
            res=requests.get(url)
            html=res.text
            Returns:

        """

        gr = grequests()
        url = "http://www.cninfo.com.cn/new/fulltextSearch/full"
        params = {'searchkey': "业绩预增",
                  'sdate': '',
                  'edate': "",
                  # 'isfulltext':'False',
                  'isfulltext': False,  # 不佳引号也可以
                  'sortName': "pubdate",
                  'sortType': "desc",
                  'pageNum': '1'
                  }
        res = grequests.get(url=url, params=params)
        self.assertTrue(res.status_code == 200)
        # print(res.content)
        j = json.loads(res.content)
        print("总页数：", j.get("totalpages"))
        print("", j.get('announcements'))
        keys = ['secCode', 'secName' ,'announcementTitle','announcementTime', 'adjunctType', 'adjunctUrl']
        print(keys)
        for item in j.get('announcements'):
            j2 = json.loads(json.dumps(item))
            if len(j2.get('secCode')) == 6:
                for key in keys:
                    print(j2.get(key), end='||')
                print("")

    def test_get_json_3(self):
        """查询巨潮资讯业务预增
            import requests
            url="http://www.cninfo.com.cn/new/fulltextSearch/full?searchkey=%E4%B8%9A%E7%BB%A9%E9%A2%84%E5%A2%9E&sdate=&edate=&isfulltext=false&sortName=pubdate&sortType=desc&pageNum=1"
            res=requests.get(url)
            html=res.text
            Returns:

        """

        gr = grequests()
        url = "http://www.cninfo.com.cn/new/fulltextSearch/full"
        # 十页
        for i in range(10):
            params = {'searchkey': "业绩预增",
                      'sdate': '',
                      'edate': "",
                      # 'isfulltext':'False',
                      'isfulltext': False,  # 不佳引号也可以
                      'sortName': "pubdate",
                      'sortType': "desc",
                      'pageNum': i
                      }
            res = grequests.get(url=url, params=params)
            self.assertTrue(res.status_code == 200)
            # print(res.content)
            j = json.loads(res.content)
            print(f'总页数：{j.get("totalpages")}')
            print("", j.get('announcements'))
            keys = ['secCode', 'secName' ,'announcementTitle','announcementTime', 'adjunctType', 'adjunctUrl']
            print(keys)
            for item in j.get('announcements'):
                j2 = json.loads(json.dumps(item))
                if len(j2.get('secCode')) == 6:
                    for key in keys:
                        print(j2.get(key), end='||')
                    print("")
