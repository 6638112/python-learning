# ip代理池
# IP地址取自国内髙匿代理IP网站：http://www.xicidaili.com/nn/
# 仅仅爬取首页IP地址就足够一般使用
import urllib3
import urllib
import random

import requests
from bs4 import BeautifulSoup

from com.dxshs.common.FileUtil import *

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Host": "www.xicidaili.com",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "Cookie": "_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTliYzJkOTU0NmExMjdiZjE0ZTJhOWQ3MDhjM2QwNjU0BjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMTFaempibllNakpzYXpyT0xFK2xpNEE1ajFldW4rbSs4emlDWWFqNEhCVnM9BjsARg%3D%3D--e8a729c035dd48f3220b7a6d7637799efc738b86; Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1560149912,1560150784; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1560150805"
}

headers2 = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Host": "www.ipip.net",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "Cookie": "_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTliYzJkOTU0NmExMjdiZjE0ZTJhOWQ3MDhjM2QwNjU0BjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMTFaempibllNakpzYXpyT0xFK2xpNEE1ajFldW4rbSs4emlDWWFqNEhCVnM9BjsARg%3D%3D--e8a729c035dd48f3220b7a6d7637799efc738b86; Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1560149912,1560150784; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1560150805"
}

HTTP_PREFIX = 'http://'

# 获取当前访问使用的IP地址网站
check_current_url = "https://www.ipip.net/"


def getHTMLText(url, proxies):
    """
    获取网页内容函数
    :param url:
    :param proxies:
    :return:
    """
    try:
        r = requests.get(url, proxies=proxies)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
    except:
        return 0
    else:
        return r.text


def get_ip_list(url):
    """
    从代理ip网站获取代理ip列表函数，并检测可用性，返回ip列表
    :param url:
    :return:
    """
    ip_list = []
    page_num = 1
    limit = 40
    while True:
        if len(ip_list) >= limit:
            break
        current_url = url + str(page_num)
        page_num += 1
        web_data = requests.get(current_url, headers=headers)
        soup = BeautifulSoup(web_data.text, 'html')
        if not soup:
            break
        ips = soup.find_all('tr')
        if not ips:
            break
        for i in range(1, len(ips)):
            ip_info = ips[i]
            tds = ip_info.find_all('td')
            time_out = tds[8].text
            if '天' not in time_out:
                continue
            ip_list.append(tds[1].text + ':' + tds[2].text)
            # 检测ip可用性，移除不可用ip：（这里其实总会出问题，你移除的ip可能只是暂时不能用，剩下的ip使用一次后可能之后也未必能用）
            for ip in ip_list:
                try:
                    proxy_host = "https://" + ip
                    proxy_temp = {"https": proxy_host}
                    requests.get(current_url, headers=headers, proxies=proxy_temp)
                    # res = urllib.request.urlopen(url, headers=headers, proxies=proxy_temp).read()
                    # print(res)
                except Exception as e:
                    ip_list.remove(ip)
                    continue
    return ip_list


def get_random_ip(ip_list):
    """
    从ip池中随机获取ip列表
    :param ip_list:
    :return:
    """
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    proxy_ip = random.choice(proxy_list)
    proxies = {'http': proxy_ip}
    return proxies


def get_random_ip_from_file(file_name='../company/ip.txt'):
    """
    从ip池中随机获取ip列表
    :param ip_list:
    :return:
    """
    ip_list = read_list(file_name)
    proxy_ip = random.choice(ip_list)
    proxies = {'HTTPS': proxy_ip}
    # proxies = {'HTTPS': proxy_ip}
    # proxies = {'http': 'http://' + proxy_ip, 'https':'https://' + proxy_ip}
    print('当前使用的代理信息：%s' % json.dumps(proxies))
    return proxies


if __name__ == '__main__':
    url = 'https://www.xicidaili.com/nn/'
    ip_list = get_ip_list(url)
    # 写出至文件
    parent_path = os.path.abspath(os.path.dirname(os.getcwd()))
    out_file_name = parent_path + '/company/ip.txt'
    write_by_line(out_file_name, ip_list, mode='w')
    proxies = get_random_ip_from_file(out_file_name)
    requests.get(check_current_url, headers=headers2, proxies=proxies)
    print(proxies)
