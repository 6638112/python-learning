import random
import time

from bs4 import BeautifulSoup
import os

from com.dxshs.common.IpUtil import get_random_ip_from_file
from com.dxshs.common.Param import *
from com.dxshs.company.intellectual_property.IntellectualProperty import get_patent_info
from com.dxshs.company.listing.ListingInformationUtil import get_listing_by_soup
from com.dxshs.company.news.News import get_news
from com.dxshs.company.operation_risk.OperatingRisk import get_operating_risk
from com.dxshs.company.operation_status.OperationStatus import get_administrative_license
from com.dxshs.company.relation.BusinessRelation import *
from com.dxshs.company.risk.JudicialRiskUtil import query_all_legal_action
from com.dxshs.tianyancha.Login2 import *
from com.dxshs.common.UserAgentUtil import *
from com.dxshs.tianyancha.OpenUtil import *

fields = ['注册资本', '成立日期', '经营状态', '工商注册号', '统一社会信用代码', '组织机构代码',
          '纳税人识别号', '公司类型', '营业期限', '行业', '纳税人资质', '核准日期', '实缴资本',
          '人员规模', '参保人数', '登记机关', '曾用名', '英文名称', '注册地址', '经营范围']

cn_en_map = {
    '公司名称': 'gsmc',
    '电话': 'dh',
    '邮箱': 'yx',
    '网址': 'wz',
    '地址': 'dz',
    '简介': 'jj',
    '注册资本': 'zczb',
    '成立日期': 'clrq',
    '经营状态': 'jyzt',
    '工商注册号': 'gszch',
    '统一社会信用代码': 'tyshxydm',
    '组织机构代码': 'zzjgdm',
    '纳税人识别号': 'nsrsbh',
    '公司类型': 'gslx',
    '营业期限': 'yyqx',
    '行业': 'hy',
    '纳税人资质': 'nsrzz',
    '核准日期': 'hzrq',
    '实缴资本': 'sjzb',
    '人员规模': 'rygm',
    '参保人数': 'cbrs',
    '登记机关': 'djjg',
    '曾用名': 'cym',
    '英文名称': 'ywmc',
    '注册地址': 'zcdz',
    '经营范围': 'jyfw',
    '法人代表': 'frdb'
}
pages = 5

citys = ['hhht', 'baotou', 'wuhai', 'chifeng', 'tongliao', 'eeds', 'hlbe', 'byne', 'wlcb', 'xam', 'xlglm', 'alsm']


# cookie = 'TYCID=eef74250836811e9b3eb7fa713b59774; undefined=eef74250836811e9b3eb7fa713b59774; ssuid=4860560592; _ga=GA1.2.65095863.1559282237; _gid=GA1.2.1767358692.1560081163; aliyungf_tc=AQAAAG/+kyEV2A4AjIabJym8kkwFsFJS; bannerFlag=undefined; csrfToken=QNfPgNCp7OeC8_-F_LV5maJI; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1560139180,1560160069,1560171802,1560234258; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522signUp%2522%253A%25220%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522lx123%2522%252C%2522integrity%2522%253A%252214%2525%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522state%2522%253A%25220%2522%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25221%2522%252C%2522monitorUnreadCount%2522%253A%25227%2522%252C%2522onum%2522%253A%25220%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzI2MTczMTI1MSIsImlhdCI6MTU2MDI0MTY1MSwiZXhwIjoxNTkxNzc3NjUxfQ.ZIqAjMz8_oHBNH3cWx4kOA2qLi3-CnxNp3ag6eogYeiSIheuVTbqrwL5pIkoyA2w4oTkOzCU8xVIoayGtew9zw%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252213261731251%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzI2MTczMTI1MSIsImlhdCI6MTU2MDI0MTY1MSwiZXhwIjoxNTkxNzc3NjUxfQ.ZIqAjMz8_oHBNH3cWx4kOA2qLi3-CnxNp3ag6eogYeiSIheuVTbqrwL5pIkoyA2w4oTkOzCU8xVIoayGtew9zw; RTYCID=7c8f07f467ae4597821d2118e3629597; CT_TYCID=6feb4f93d5514286a574ec43a4b616f9; cloud_token=ff7c5520c4e14eb785c0eb36269a186b; cloud_utm=517ae4e9d9c34c7494347148e858f048; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1560302343'

# cookie = 'CT_TYCID=f373236dfefb4b87a7d8dd583990a043; cloud_token=084bf54a02b84f2084ac9b2ba2de3ee4; cloud_utm=71e3e4c41cec4ae88a71cc9be8169924; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1560247589; RTYCID=eb5b7742a3be4cb4b363e46c7b125857; _gat_gtag_UA_123487620_1=1; _gid=GA1.2.153805045.1560161282; bannerFlag=true; _utm=8173a9300a454d20a0fbb07f1523d87e; token=f0d9cda48a7748a6a684c8592f2379c3; csrfToken=ook-HLW9AxD-sjK1HQPamX1u; aliyungf_tc=AQAAAIIsOjTwKQ0AjIabJ4DCxbdxSa9O; TYCID=79dd07108b2511e99959dba726b6cb09; undefined=79dd07108b2511e99959dba726b6cb09; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1560161282,1560161304,1560161314,1560234983; _ga=GA1.2.926897394.1560161282; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzkyNjI3ODgxNCIsImlhdCI6MTU2MDI0NzU1MiwiZXhwIjoxNTkxNzgzNTUyfQ.KeCMTw0BxuWz3HLN9SlbEPjW5h4WR32aF43RDUw04_dxoGPY2mlScVW-fEBuxBiS09Y6-cMCG4zrBC8dGMPcqQ; ssuid=4727556104; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522signUp%2522%253A%25220%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E7%258F%25AD%25E5%25A9%2595%25E5%25A6%25A4%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522state%2522%253A%25220%2522%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzkyNjI3ODgxNCIsImlhdCI6MTU2MDI0NzU1MiwiZXhwIjoxNTkxNzgzNTUyfQ.KeCMTw0BxuWz3HLN9SlbEPjW5h4WR32aF43RDUw04_dxoGPY2mlScVW-fEBuxBiS09Y6-cMCG4zrBC8dGMPcqQ%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252213926278814%2522%257D'
SPLIT_STR = '|'

SEPARATION_CHARACTER = '|'

# cookie是否过期
IS_COOKIE_TIMEOUT = False

parent_path = os.path.abspath(os.path.dirname(os.getcwd()))
print('parent_path:{}'.format(parent_path))


def read_cookie(cookie_file_name = './cookie.txt'):
    """
    从文件中读取cookie
    :param cookie_file_name:
    :return:
    """
    cookie_list = read_list(cookie_file_name)
    if cookie_list:
        return cookie_list[0]

cookie = read_cookie()

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Host": "www.tianyancha.com",
    "Upgrade-Insecure-Requests": "1",
    "Referer": "https://www.tianyancha.com/search",
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    "Cookie": cookie
}


def get_soup(url, headers, proxies):
    begin = time.time();
    # print('查询url：%s开始...' % url)
    response = requests.get(url, headers=headers, proxies=proxies)
    response.encoding = 'utf-8'
    if response.status_code != 200:
        print(response.status_code)
        print('查询简介异常')
    soup = BeautifulSoup(response.text, 'lxml')
    # print('查询结束，耗时：%f秒' % (time.time() - begin))
    return soup


def get_url_list():
    """
    获取公司url列表
    :param url:https://www.tianyancha.com/search?base=nmg
    :return:
    """
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "www.tianyancha.com",
        "Upgrade-Insecure-Requests": "1",
        "Referer": "https://www.tianyancha.com/search",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        "Cookie": cookie
    }
    url_list = [];
    for city in citys:
        for i in range(pages):
            page = i + 1;
            url = 'https://www.tianyancha.com/search/p' + str(page) + '?base=' + city
            print('开始查询城市：%s第%d页数据，url：%s' % (city, page, url))
            proxies = get_random_ip_from_file()
            soup = get_soup(url, headers, proxies)
            contents = soup.find_all(class_='name select-none')
            if not contents:
                contents = soup.find_all(class_='name')
            persons = soup.find_all(class_='legalPersonName')
            if contents:
                for content in contents:
                    href = content.attrs['href']
                    # print('href：%s' % href)
                    url_list.append(href)
        print('%s查询出公司个数：%d' % (city, len()))
    return url_list


def get_legal_name_by_url():
    """
    获取公司url列表
    :param url:https://www.tianyancha.com/search?base=nmg
    :return:
    """
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "www.tianyancha.com",
        "Upgrade-Insecure-Requests": "1",
        "Referer": "https://www.tianyancha.com/search",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        "Cookie": cookie
    }
    result = {};
    country_code = read_json('./country_code.json')
    for city, countrys in country_code.items():
        count = 0
        for i in range(pages):
            for country in countrys:
                page = i + 1;
                url = 'https://www.tianyancha.com/search/p' + str(page) + '?base=' + city + '&areaCode=' + str(
                    country['country_code'])
                print('开始查询城市：%s第%d页数据，url：%s' % (city, page, url))
                proxies = get_random_ip_from_file()
                soup = get_soup(url, headers, proxies)
                companys = soup.find_all(attrs={'tyc-event-ch': "CompanySearch.Company"})
                # legal_persons = soup.find_all(class_='legalPersonName')
                legal_persons = [person.text.replace('法定代表人：', '').replace('未公开', '') for person in
                                 soup.find_all(class_='title text-ellipsis') if '法定代表人' in person.text]
                legal_persons = soup.find_all(class_='title text-ellipsis')[::2]
                if len(legal_persons) < len(companys):
                    print("url:%s查询出法人信息有误！it's error." % url)
                    continue
                if companys:
                    for j in range(len(companys)):
                        company = companys[j]
                        href = company.attrs['href']
                        legal_name = legal_persons[j].text
                        legal_name = legal_name.split('：')[1].replace('未公开', '')
                        result[href] = legal_name
                        with open('./url_list.txt', 'a') as file:
                            file.write(href + '|' + legal_name + '\n')
                        count += 1
            time.sleep(1)
            # print('href：%s' % href)
        print('%s查询出公司个数：%d' % (city, count))
    return result


def get_brief(url, proxies):
    """
    获取简介
    :return:
    """
    begin = time.time();
    print('url：%s，查询简介开始...' % url)
    response = requests.get(url, headers=headers, proxies=proxies)
    # print('查询简介的ip地址：%s' % response.raw._connection.sock.getpeername()[0])
    response.encoding = 'utf-8'
    if response.status_code != 200:
        status_code = response.status_code
        print(status_code)
        print('查询简介异常')
        global IS_COOKIE_TIMEOUT
        IS_COOKIE_TIMEOUT = True
        print('cookie过期，请重新登录，已中断查询！')

    soup = BeautifulSoup(response.text, 'lxml')
    business_information = get_business_information(soup)
    if len(business_information) == 0:
        return business_information;
    official_information = get_official_information(soup)
    for key, value in official_information.items():
        business_information[key] = value

    # for content in lines:
    #     value = content.tr.td.contents[0] if content.tr.td.contents[0] else '';
    #     print('value:%s', value);
    print('查询简介结束，耗时%f秒' % (time.time() - begin))

    return business_information;


def get_business_information(soup):
    """
    工商信息
    :param soup:
    :return:
    """
    data = {}
    try:
        contents = soup.find_all(class_='table -striped-col -border-top-none -breakall')[0].contents;
        items = []
        if len(contents):
            lines = contents[0].find_all('tr')
            for line in lines:
                columns = line.find_all('td')
                for column in columns:
                    text = column.getText()
                    # print(text)
                    if text:
                        items.append(text)

        for i, item in enumerate(items):
            if i % 2 == 0:
                value = items[i + 1]
                if value == '-':
                    value = ''
                data[item] = value
    except Exception as error:
        print(error)
        return data
    return data


def get_official_information(soup):
    """
    官方信息，获取公司名称、电话、邮箱、网址、地址、简介等
    :param soup:
    :return:
    """
    info = {}
    # 公司名称
    name = soup.h1.contents[0]
    print('公司名称：%s' % name)
    info['公司名称'] = name
    lines = soup.find_all(class_='detail')[0].contents
    for line_num in range(len(lines)):
        line = lines[line_num]
        if line.name:
            columns = line.contents
            for column in columns:
                tags = column.contents
                for i in range(len(tags)):
                    try:
                        if line_num < 3:
                            content = tags[i].contents[0]
                        else:
                            brief = tags[0];
                            brief = brief.replace('简介：', '').strip().strip('\n').replace('〓... 更多', '').replace(
                                '... 更多', '')
                            brief = brief.replace('暂无信息', '')
                            info['简介'] = brief
                            return info
                        key = ''
                        if i + 1 >= len(tags):
                            break
                        if '网址' in content or '地址' in content:
                            value = tags[2].contents[0]
                        else:
                            value = tags[i + 1].contents[0]
                        if '电话' in content:
                            key = '电话'
                        elif '邮箱' in content:
                            key = '邮箱'
                        elif '网址' in content:
                            key = '网址'
                        elif '地址' in content:
                            key = '地址'
                        elif '简介' in content:
                            key = '简介'
                        if key:
                            value = value.strip().strip('\n').replace('暂无信息', '')
                            if value == '-':
                                value = ''
                            info[key] = value
                            break
                    except Exception as error:
                        print(error)
                        info[key] = ''
    return info;


def convert(info):
    """
    字段翻译
    :param info:
    :return:
    """
    result = {}
    for key, value in cn_en_map.items():
        if key in info:
            result[value] = replace_redundancy_character(info[key])
        else:
            result[value] = ''
    return result


def convert_to_str(template_file, info, separation='|'):
    """
    字典转字符串
    :param template_file:
    :param info:
    :param separation:
    :return:
    """
    template = read_json(template_file)
    data = []
    for k, v in template.items():
        if k in info:
            data.append(info[k])
        else:
            data.append('')
    return separation.join(data)


def replace_redundancy_character(str):
    """
    去掉多余字符
    :param str:
    :return:
    """
    if str:
        str = str.replace('〓... 更多', '').replace('... 更多', '')
    return str


def get_risk(url):
    """
    风险
    :return:
    """
    return;


# initTime: function(t)
# {
# return moment(parseInt(t)).utcOffset(8).format("YYYY-MM-DD")
# }

def read_url_legal_name_map(url_file_name):
    """
    url对应法人的map
    :param url_file_name:
    :return:
    """
    exist_url_legal_name_list = read_list(url_file_name)
    # url对应法人的map
    # url_legal_name_map = get_legal_name_by_url()
    url_legal_name_map = {}
    for url_legal_name in exist_url_legal_name_list:
        url = url_legal_name.split(SPLIT_STR)[0]
        legal_name = url_legal_name.split(SPLIT_STR)[1]
        if url not in url_legal_name_map:
            url_legal_name_map[url] = legal_name
    return url_legal_name_map


def distinct(url_file_name):
    """
    url文件数据去重
    :param url_file_name:
    :return:
    """
    exist_url_legal_list = read_list(url_file_name)
    # url对应法人的map
    # url_legal_name_map = get_legal_name_by_url()
    url_legal_name_map = read_url_legal_name_map(url_file_name)
    lines = []
    for k, v in url_legal_name_map.items():
        line = k + SPLIT_STR + v
        lines.append(line)
    write_by_line(url_file_name, lines, mode='w')


def get_business_relation(base_url, company_id):
    """
    查询企业关系
    :param base_url:
    :param company_id:
    :return:
    """
    url = base_url + str(company_id) + '.json'
    print('查询企业关系url：%s' % url)
    headers = {}
    url_relation_map = {}
    data = requests.get(url, headers=headers)
    url_relation_map[company_id] = data
    return url_relation_map


def generate_related_info(url_list):
    """
    生成级联信息
    :param url_list:
    :return:
    """
    # 已查询过的url文件名
    queried_url_file_name = './queried_url.txt'
    # 读取已查询过的url列表
    queried_url_list = read_queried_url_list(queried_url_file_name)
    if queried_url_list:
        url_list = [item for item in url_list if not item in queried_url_list]

    count = 0
    cookie_flag = True
    for url in url_list:
        proxies = get_random_ip_from_file()
        base_info = query_base_info(url, proxies)
        items = url.split('/')
        company_id = items[-1]
        # if IS_COOKIE_TIMEOUT:
        #     print('cookie过期，执行中断，当前待查询url：%s' % url)
        #     update_cookie()
        #     base_info = query_base_info(url)
        #     items = url.split('/')
        #     company_id = items[-1]
        #     break
        company_name = base_info['gsmc']
        # if count > 0 and count % 48 == 0:
        #     print('查询公司个数：%d，开始线程等待...' % count)
        #     if cookie_flag:
        #         headers['Cookie'] = cookie2
        #         cookie_flag = False
        #     else:
        #         headers['Cookie'] = cookie
        #         cookie_flag = True
        # if not company_name:
        #     continue
        while not company_name:
            print('公司名称为空，执行中断，需要手动通过验证码！查询公司个数：%d。请更新cookie值！' % count)
            cookie = login()
            write_cookie(cookie)
            headers['Cookie'] = cookie
            base_info = query_base_info(url, proxies)
            items = url.split('/')
            company_id = items[-1]
            company_name = base_info['gsmc']

        template_file_name = './templates/companyTemplate.json'
        out_file_name = os.getcwd() + '/data/companyData.csv'
        write_json_without_title(template_file_name, out_file_name, base_info,
                                 separation_character=SEPARATION_CHARACTER, mode='a')

        soup = get_soup(url, headers=headers, proxies=proxies)
        # 上市信息-发行相关
        listing_info(company_id, company_name, soup)

        # 司法风险-法律诉讼
        law_case(company_id, company_name)

        # 经营风险-股权出质
        operating_risk(company_id, company_name)

        # 经营状况-行政许可
        administrative_license(company_id, company_name)
        # time.sleep(random.randint(1, 2))

        # 知识产权-专利信息
        patent_info(company_id, company_name)

        # 新闻舆情
        news_info(company_id, company_name, separation_character='|-|')

        # 企业关系
        # business_relation(company_id, company_name)
        print('-----------------------------------------------')

        # 写文件
        write_queried_url(queried_url_file_name, url + '\n', mode='a')
        count += 1
        time.sleep(random.randint(1, 3))


def listing_info(company_id, company_name, soup, separation_character=SEPARATION_CHARACTER):
    """
    上市信息-发行相关
    :param company_id:
    :param soup:
    :param separation_character:
    :return:
    """
    listing_info = get_listing_by_soup(soup)
    if listing_info:
        table_name = 'listingInfo'
        template_file_name = get_default_template_file_name(table_name)
        out_file_name = get_default_out_file_name(company_name, table_name)
        write_json_without_title(template_file_name, out_file_name, listing_info, separation_character, mode='a+')
    else:
        print_empty_message(company_id, company_name, '上市信息-发行相关')


def law_case(company_id, company_name, separation_character=SEPARATION_CHARACTER):
    """
    司法风险-法律诉讼
    :param company_id:
    :param soup:
    :param separation_character:
    :return:
    """
    # 司法风险-法律诉讼
    pagination_risk_base_url = 'https://www.tianyancha.com/pagination/lawsuit.xhtml'
    law_param = Param(pagination_risk_base_url, company_id, company_name)
    law_case_list = query_all_legal_action(law_param, headers)

    # template_file_name = './templates/riskTemplate.json'
    # out_file_name = './data/' + company_name + '/riskData.csv'
    if law_case_list:
        table_name = 'lawRiskInfo'
        template_file_name = get_default_template_file_name(table_name)
        out_file_name = get_default_out_file_name(company_name, table_name)
        write_list_map_without_title(template_file_name, out_file_name, law_case_list, separation_character, mode='a+')
    else:
        print_empty_message(company_id, company_name, '司法风险-法律诉讼')


def operating_risk(company_id, company_name, separation_character=SEPARATION_CHARACTER):
    """
    经营风险-股权出质
    :param company_id:
    :param soup:
    :param separation_character:
    :return:
    """
    # 经营风险-股权出质
    pagination_equity_base_url = 'https://www.tianyancha.com/pagination/equity.xhtml'
    operating_risk_param = Param(pagination_equity_base_url, company_id, company_name)
    operating_risk_list = get_operating_risk(operating_risk_param, headers)

    # template_file_name = './templates/operatingRiskTemplate.json'
    # out_file_name = './data/' + company_name + '/operatingRiskData.csv'
    if operating_risk_list:
        table_name = 'operationRiskInfo'
        template_file_name = get_default_template_file_name(table_name)
        out_file_name = get_default_out_file_name(company_name, table_name)
        write_list_map_without_title(template_file_name, out_file_name, operating_risk_list, separation_character,
                                     mode='a+')
    else:
        print_empty_message(company_id, company_name, '经营风险-股权出质')


def administrative_license(company_id, company_name, separation_character=SEPARATION_CHARACTER):
    """
    经营状况-行政许可
    :param company_id:
    :param soup:
    :param separation_character:
    :return:
    """
    # 经营状况-行政许可
    pagination_licensing_base_url = 'https://www.tianyancha.com/pagination/licensing.xhtml'
    administrative_license_param = Param(pagination_licensing_base_url, company_id, company_name)
    administrative_license_list = get_administrative_license(administrative_license_param, headers)

    # template_file_name = './templates/operationStatusTemplate.json'
    # out_file_name = './data/' + company_name + '/operationStatusData.csv'
    if administrative_license_list:
        table_name = 'operationStatusInfo'
        template_file_name = get_default_template_file_name(table_name)
        out_file_name = get_default_out_file_name(company_name, table_name)
        write_list_map_without_title(template_file_name, out_file_name, administrative_license_list,
                                     separation_character, mode='a+')
    else:
        print_empty_message(company_id, company_name, '经营状况-行政许可')


def patent_info(company_id, company_name, separation_character=SEPARATION_CHARACTER):
    """
    知识产权-专利信息
    :param company_id:
    :param soup:
    :param separation_character:
    :return:
    """
    # 知识产权-专利信息
    pagination_patent_base_url = 'https://www.tianyancha.com/pagination/patent.xhtml'
    patent_param = Param(pagination_patent_base_url, company_id, company_name)
    patent_list = get_patent_info(patent_param, headers)

    # template_file_name = './templates/intellectualPropertyTemplate.json'
    # out_file_name = './data/' + company_name + '/intellectualPropertyData.csv'
    if patent_list:
        table_name = 'patentInfo'
        template_file_name = get_default_template_file_name(table_name)
        out_file_name = get_default_out_file_name(company_name, table_name)
        write_list_map_without_title(template_file_name, out_file_name, patent_list, separation_character, mode='a+')
    else:
        print_empty_message(company_id, company_name, '知识产权-专利信息')


def news_info(company_id, company_name, separation_character=SEPARATION_CHARACTER):
    """
    新闻舆情
    :param company_id:
    :param soup:
    :param separation_character:
    :return:
    """
    # 新闻舆情
    news_base_url = 'https://www.tianyancha.com/pagination/findNewsCount.xhtml'
    news_param = Param(news_base_url, company_id, company_name)
    news_list = get_news(news_param, headers)

    # template_file_name = './templates/newsTemplate.json'
    # out_file_name = './data/' + company_name + '/newsData.csv'
    if news_list:
        table_name = 'newsInfo'
        template_file_name = get_default_template_file_name(table_name)
        out_file_name = get_default_out_file_name(company_name, table_name)
        write_list_map_without_title(template_file_name, out_file_name, news_list, separation_character, mode='a+')
    else:
        print_empty_message(company_id, company_name, '新闻舆情')


def business_relation(company_id, company_name):
    """
    企业关系
    :param company_id:
    :param company_name:
    :param separation_character:
    :return:
    """
    base_url = 'https://dis.tianyancha.com/dis/getInfoById/'
    out_file_name = './data/businessRelationData/' + company_id + '.json'
    # out_file_name = './data/' + company_name + '/businessRelationData.json'
    data = get_business_relation_str(base_url, company_id, headers)
    if data:
        write_str(out_file_name, data, mode='w')
    else:
        print_empty_message(company_id, company_name, '企业关系')


def get_default_template_file_name(table_name):
    """
    获取默认模板文件名（全路径）
    :param table_name:
    :return:
    """
    # 当前工作目录：'/Users/liuxian/PycharmProjects/FlaskProject/com/dxshs/company'
    home_path = os.getcwd()
    template_file_name = home_path + '/templates/' + table_name + 'Template.json'
    print('模板文件：%s' % template_file_name)
    return template_file_name


def get_default_out_file_name(company_name, table_name):
    """
    获取默认数据文件名（全路径）
    :param company_name:
    :param table_name:
    :return:
    """
    home_path = os.getcwd()
    out_file_name = home_path + '/data/' + company_name + '/' + table_name + 'Data.csv'
    print('数据文件：%s' % out_file_name)
    return out_file_name


def print_empty_message(company_id, company_name, type):
    """
    打印消息
    :param company_id:
    :param company_name:
    :param type:
    :return:
    """
    print('编号：%s，名称：%s，对应的公司查询出%s为空！' % (str(company_id), company_name, type))


def query_base_info(url, proxies):
    """
    查询基本信息
    :param url:
    :return:
    """
    brief = get_brief(url, proxies)
    brief['法人代表'] = url_legal_name_map.get(url) if url in url_legal_name_map else ''
    info = convert(brief)
    return info


def write_queried_url(out_file_name, data, mode='a'):
    """
    更新已查询过的url
    :param out_file_name:
    :param data:
    :param mode:
    :return:
    """
    write_str(out_file_name, data, mode)


def read_queried_url_list(file_name):
    """
    读取已查询过的url
    :param file_name:
    :return:
    """
    url_list = read_list(file_name)
    return url_list


def update_cookie():
    """
    更新cookie
    :return:
    """
    # global cookie
    global headers
    global IS_COOKIE_TIMEOUT
    cookie = get_cookie()
    print('获取新的cookie：%s' % cookie)
    headers['Cookie'] = cookie
    IS_COOKIE_TIMEOUT = False


def write_cookie(data, cookie_file_name = './cookie.txt', mode='w'):
    """
    写cookie
    :param cookie_file_name:
    :return:
    """
    write_str(cookie_file_name, data, mode)


if __name__ == '__main__':
    # timeStamp = 39171337
    # timeArray = time.localtime(timeStamp)
    # otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    # print(otherStyleTime)
    #
    # t = time.strptime('2018-12-28', '%Y-%m-%d')
    # time.mktime(t)
    # url_file_name = '../company/child_company_url_list.txt';
    url_file_name = '../company/url_list_bak.txt'
    # distinct(url_file_name)
    # url = 'https://www.tianyancha.com/company/24416401';
    # exist_url_legal_list = read_list(url_file_name)

    # url_legal_name_map = {
    #     'https://www.tianyancha.com/company/11997559': '管连平'
    # }
    url_legal_name_map = read_url_legal_name_map(url_file_name)
    url_list = list(url_legal_name_map.keys())
    generate_related_info(url_list)

    # url对应法人的map
    # url_legal_name_map = get_legal_name_by_url()
    # url_list = list(set(url_list + exist_url_list))
    # write_by_line(file_name, url_list, mode='w');
    # with open('./legal_name.json', 'w') as file:
    #     file.write(url_legal_name_map)
    # url_list = ['https://www.tianyancha.com/company/24416401']

    template_file = './companyTemplate.json'
    data_file = './companyData.csv'

    # lines = []
    # for url in url_list:
    #     brief = get_brief(url)
    #     if len(brief) == 0:
    #         print('url：%s查询异常，数据查询失败' % url)
    #         continue
    #     brief['法人代表'] = url_legal_name_map.get(url) if url in url_legal_name_map else ''
    #     info = convert(brief)
    #     line = convert_to_str(template_file, info, SPLIT_STR)
    #     line += '\n'
    #     lines = [line]
    #     write_by_line(data_file, lines, 'a')
    #     time.sleep(1)

    # if len(lines):
    #     write_by_line(data_file, lines, 'a')
