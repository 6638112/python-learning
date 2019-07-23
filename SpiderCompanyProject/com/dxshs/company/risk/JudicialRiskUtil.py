# 司法风险-法律诉讼
import os

from com.dxshs.common.CrawlerUtils import *
from com.dxshs.common.FileUtil import *
from com.dxshs.common.Param import *

template_file_name = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '/templates/lawRiskInfoTemplate.json'
out_file_name = './riskData.csv'
# 分隔符
SEPARATION_CHARACTER = '|'

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Host": "www.tianyancha.com",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "Cookie": "aliyungf_tc=AQAAANebsQWLswAAjIabJ/cMIq4ikFgO; csrfToken=CUlblbPZqr1cdp9Om2HeKm1d; TYCID=eef74250836811e9b3eb7fa713b59774; undefined=eef74250836811e9b3eb7fa713b59774; ssuid=4860560592; _ga=GA1.2.65095863.1559282237; bannerFlag=true; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1559284159,1559284270,1559286829,1559287410; RTYCID=82bd3af1b3ef4539af5b36de69dc2a2b; CT_TYCID=c6561b23d2494d9f9a9690e4a8c488a6; _gid=GA1.2.1787049886.1559526377; token=b37f2d0862924836a77223fb3216fd8e; _utm=0cf78922917642c78561f71858a40858; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522signUp%2522%253A%25221%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E5%2588%2598%25E5%25BD%25BB%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522state%2522%253A%25220%2522%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522new%2522%253A%25221%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzI2MTczMTI1MSIsImlhdCI6MTU1OTU0MDQ5MCwiZXhwIjoxNTkxMDc2NDkwfQ.eYxGlYdscCrQINCrMcrnE-poJHqRo6EFKgnBSx-oSS0hva_i_3WDYmfJxyXndPeYGHnwOdEbFb5o5H4-4f0Pfw%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252213261731251%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzI2MTczMTI1MSIsImlhdCI6MTU1OTU0MDQ5MCwiZXhwIjoxNTkxMDc2NDkwfQ.eYxGlYdscCrQINCrMcrnE-poJHqRo6EFKgnBSx-oSS0hva_i_3WDYmfJxyXndPeYGHnwOdEbFb5o5H4-4f0Pfw; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1559627166; cloud_token=13fcb96bc2fc411a94d542e7502145ba"
}
pagination_risk_base_url = 'https://www.tianyancha.com/pagination/lawsuit.xhtml'


class Case(object):
    def __init__(self, date, case_name, cause_of_action, case_status, case_num, detail_url):
        self.rq = date
        self.ajmc = case_name
        self.ay = cause_of_action
        self.ajsf = case_status
        self.ah = case_num
        self.xq = detail_url


# class LawsuitParam(object):
#     def __init__(self, base_url, name, pn=1, ps=500):
#         self.base_url = base_url
#         self.name = name
#         self.pn = pn
#         self.ps = ps
#
#     def get_url(self):
#         url = self.base_url + '?' + 'pn=' + str(self.pn) + '&ps=' + str(self.ps) + '&name=' + self.name
#         return url


def get_current_page_legal_action(url, headers=headers):
    """
    法律诉讼
    :param url:
    :param headers:
    :return:
    """
    # fields = ['日期', '案件名称', '案由', '案件身份', '案号']
    template_map = read_json(template_file_name)
    fields = list(template_map.keys())
    soup = get_soup(url, headers)
    # soup.find_all(attrs = {'event-name':'企业详情-法律诉讼'})
    case_list = []
    container = soup.find_all(id='_container_lawsuit')
    if container:
        contents = container[0].next.contents
        if len(contents) > 1:
            # 所有的行
            lines = contents[1].contents
            for line in lines:
                # 所有的列
                columns = line.contents
                if len(columns) != 6:
                    print('查询出法律诉讼信息列不正确，共%d列' % len(columns))
                    continue
                try:
                    # 日期
                    date = columns[1].text
                    # 案件名称
                    case_name = columns[2].text
                    # 案由
                    cause_of_action = columns[3].text
                    # 案件身份
                    case_status = columns[4].text
                    # 案号
                    case_num = columns[5].text
                    # 详情
                    detail_url = columns[2].contents[0].attrs['href']
                    case = Case(date, case_name, cause_of_action, case_status, case_num, detail_url)
                    case_info = case.__dict__
                    case_list.append(case_info)
                except Exception as error:
                    print(error)
    return case_list


def query_all_legal_action(param, headers=headers):
    """
    查询所有法律诉讼
    :param lawsuitParam:
    :param headers:
    :return:
    """
    case_list = []
    url = param.get_url_by_company_name()
    soup = get_soup(url=url, headers=headers)
    if not soup:
        print('url：%s查询出法律诉讼信息为空' % url)
        return case_list
    while soup:
        try:
            table = soup.find(class_='table').contents
        except Exception as error:
            break
        if table and len(table) > 1:
            # 所有的行
            lines = table[1].contents
            print('url：%s，查询出法律诉讼信息记录条数：%d条' % (url, len(lines)))
            for line in lines:
                # 所有的列
                columns = line.contents
                if len(columns) != 6:
                    print('查询出法律诉讼信息列不正确，共%d列' % len(columns))
                    continue
                try:
                    # 日期
                    date = columns[1].text
                    # 案件名称
                    case_name = columns[2].text
                    case_name = case_name.replace('\n', '')
                    # 案由
                    cause_of_action = columns[3].text
                    cause_of_action = cause_of_action.replace('\n', '')
                    # 案件身份
                    case_status = columns[4].text
                    # 案号
                    case_num = columns[5].text
                    # 详情
                    detail_url = columns[2].contents[0].attrs['href']
                    case = Case(date, case_name, cause_of_action, case_status, case_num, detail_url)
                    case_info = case.__dict__
                    case_list.append(case_info)
                except Exception as error:
                    print(error)
        current_num = param.pn + 1
        param.pn = current_num
        url = param.get_url_by_company_name()
        soup = get_soup(url=url, headers=headers)
    return case_list


if __name__ == '__main__':
    company_id = '11997559'
    company_name = '北京东方国信科技股份有限公司'
    param = Param(pagination_risk_base_url, company_id=company_id, company_name=company_name, pn=1, ps=500)
    case_list = query_all_legal_action(param)
    write_list_map_with_title(template_file_name, out_file_name, case_list, SEPARATION_CHARACTER, mode='a')
    # url = 'https://www.tianyancha.com/company/3116889208'
    # case_list = get_current_page_legal_action(url)
    # print(case_list)
