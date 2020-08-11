# -*- coding: utf-8 -*-
# 加入项目根目录路径
import os.path as path
import sys

BASE_DIR = path.dirname(path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)
