#-*- coding = utf-8 -*-
#@Time : 2022/2/11 10:24
#@Author : BAYERN
#@File : test.py
#@software: PyCharm

import datetime
import re
import json


chapter_name_1 = '001 章节名'
chapter_name_2 = "第1章 章节名"

a = re.match(r'^第',chapter_name_1)
b = re.match(r'^第',chapter_name_2)
print(a,b)