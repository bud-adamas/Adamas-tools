#! /usr/bin/env python
#coding=utf-8
import urllib2
import urllib
import cookielib
data={"email":"用户名","password":"密码"}  #登陆用户名和密码
post_data=urllib.urlencode(data)
cj=cookielib.CookieJar()
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
headers ={"User-agent":"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1"}
req=urllib2.Request("http://www.renren.com/PLogin.do",post_data,headers)
content=opener.open(req)
print content.read().decode("utf-8")
