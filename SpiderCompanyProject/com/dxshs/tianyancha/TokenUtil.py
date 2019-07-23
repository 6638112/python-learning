import requests
import json
import hashlib

Phone = '13926278814'
Password = 'liubing0220'

h1 = hashlib.md5()
h1.update(Password.encode('utf-8'))
PasswordMd5 = h1.hexdigest()


def post_url():
    url = 'https://www.tianyancha.com/cd/login.json'

    header = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '253',
        'Content-Type': 'application/json; charset=UTF-8',
        'Cookie': 'Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1560235300; bannerFlag=true; _gid=GA1.2.153805045.1560161282; csrfToken=ook-HLW9AxD-sjK1HQPamX1u; aliyungf_tc=AQAAAIIsOjTwKQ0AjIabJ4DCxbdxSa9O; TYCID=79dd07108b2511e99959dba726b6cb09; undefined=79dd07108b2511e99959dba726b6cb09; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1560161282,1560161304,1560161314,1560234983; _ga=GA1.2.926897394.1560161282; ssuid=4727556104',
        'Host': 'www.tianyancha.com',
        'Origin': 'https://www.tianyancha.com',
        'Referer': 'https://www.tianyancha.com/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    login_info = {
        'autoLogin': 'true',
        'cdpassword': PasswordMd5,
        'loginway': 'PL',
        'mobile': Phone
    }
    result = requests.post(url, data=json.dumps(login_info), headers=header, verify=False)
    print(result)
    print(result.content)
    print(result.text)
    return eval(result.text)['data']['token']

if __name__ == '__main__':
    post_url()