import requests
import time
from bs4 import BeautifulSoup

from com.dxshs.common.IpUtil import get_random_ip_from_file


def get_soup(url, headers):
    """
    查询url获取网页源码
    :param url:
    :param headers:
    :return:
    """
    begin = time.time();
    # print('查询url：%s开始...' % url)
    proxies = get_random_ip_from_file()
    response = requests.get(url, headers=headers, proxies=proxies)
    # print('查询关联信息的ip地址：%s' % response.raw._connection.sock.getpeername()[0])
    response.encoding = 'utf-8'
    if response.status_code != 200:
        print(response.status_code)
        print('查询异常')
    soup = BeautifulSoup(response.text, 'lxml')
    # print('查询结束，耗时：%f秒' % (time.time() - begin))
    return soup
