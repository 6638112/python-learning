from __future__ import print_function, unicode_literals
import requests
import time
import re
import json

session = requests.session()
# session.cookies.set("tnet", "218.108.215.127")

index_url = "http://www.tianyancha.com/company/150041670"
tongji_url = "http://www.tianyancha.com/tongji/150041670.json?random=%s" % (int(time.time()) * 1000)
api_url = "http://www.tianyancha.com/company/150041670.json"

public_headers = {
        "User-Agent": "User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36",
        }

api_headers = public_headers.copy()
api_headers.update({
        "Tyc-From": "normal",
        "Accept": "application/json, text/plain, */*",
        "Referer": index_url,
        "CheckError": "check",
    })


# 访问首页
index_page = session.request("GET", index_url, headers = public_headers)


# 访问js取出_sgAtt
js_url = re.findall(r"http\:\/\/static\.tianyancha.com/wap/resources/js/\w+\.js", index_page.content)[0]
js_page = session.request("GET", js_url, headers = public_headers)
sgattrs = json.loads(re.findall(r"n\._sgArr=(.+?);", js_page.content)[0])

# 取得token和fxckStr
tongji_page = session.request("GET", tongji_url, headers = api_headers)
js_code = "".join([ chr(int(code)) for code in tongji_page.json()["data"]["v"].split(",") ])
token = re.findall(r"token=(\w+);", js_code)[0]
print("token:", token)

fxck_chars = re.findall(r"\'([\d\,]+)\'", js_code)[0].split(",")
sogou = sgattrs[9] # window.$SoGou$ = window._sgArr[9]
utm = "".join([sogou[int(fxck)] for fxck in fxck_chars])    # if(window.wtf){var fxck = window.wtf().split(",");var fxckStr = "";for(var i=0;i<fxck.length;i++){fxckStr+=window.$SoGou$[fxck[i]];}document.cookie = "_utm="+fxckStr+";path=/;";window.wtf = null;}
print("utm:", utm)

session.cookies.set("token", token)
session.cookies.set("_utm", utm)

r = session.request("GET", "http://www.tianyancha.com/IcpList/150041670.json",
        headers = api_headers)
print(r.content)

api_page = session.request("GET", api_url, headers = api_headers)
print(api_page.content)