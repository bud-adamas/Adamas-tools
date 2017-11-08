#!/usr/bin/python
#  -*- coding: utf-8 -*-

import urllib2
import urllib
import cookielib
import re

auth_url = 'http://www.nowamagic.net/'
home_url = 'http://www.nowamagic.net/';
# 登陆用户名和密码
data={
  "username":"nowamagic",
  "password":"pass"
}
# urllib进行编码
post_data=urllib.urlencode(data)
# 发送头信息
headers ={
  "Host":"www.nowamagic.net", 
  "Referer": "http://www.nowamagic.net"
}
# 初始化一个CookieJar来处理Cookie
cookieJar=cookielib.CookieJar()
# 实例化一个全局opener
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
# 获取cookie
req=urllib2.Request(auth_url,post_data,headers)
result = opener.open(req)
# 访问主页 自动带着cookie信息
result = opener.open(home_url)
# 显示结果
print result.read()
