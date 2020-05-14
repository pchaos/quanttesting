# -*- coding: utf-8 -*-
import datetime


def str2date(dateStr, format='%Y-%m-%d'):
    if isinstance(dateStr, str):
        return datetime.datetime.strptime(dateStr, format)
    else:
        return dateStr

def date2str(startdate, format='%Y-%m-%d'):
    if isinstance(startdate, datetime.datetime):
        startdate = startdate.strftime(format)
    return startdate

#检验是否全是中文字符
def is_all_chinese(strs):
    for _char in strs:
        if not '\u4e00' <= _char <= '\u9fa5':
            return False
    return True

#检验是否含有中文字符
def is_contains_chinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False