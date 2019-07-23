# 经营风险-股权出质
import requests
import os

from com.dxshs.common.CrawlerUtils import *
from com.dxshs.common.FileUtil import *
from com.dxshs.common.Param import *

template_file_name = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '/templates/operationRiskInfoTemplate.json'
out_file_name = './operatingRiskData.csv'
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


class StockRight(object):
    __doc__ = '股权信息'

    def __init__(self, gsrq, djbh, czr, zqr, zt, czgqse):
        self.gsrq = gsrq
        self.djbh = djbh
        self.czr = czr
        self.zqr = zqr
        self.zt = zt
        self.czgqse = czgqse


def get_operating_risk(param, headers=headers):
    """
    查询股权出质信息
    :param commonParam:
    :param headers:
    :return:
    """
    operating_risk_list = []
    url = param.get_url_by_company_name()
    soup = get_soup(url=url, headers=headers)
    if not soup:
        print('url：%s查询出股权出质信息为空' % url)
        return operating_risk_list
    while soup:
        try:
            table = soup.find(class_='table').contents
        except Exception as error:
            break
        if table and len(table) > 1:
            # 所有的行
            lines = table[1].contents
            if not lines:
                break
            print('url：%s，查询出经营风险-股权出质信息记录条数：%d条' % (url, len(lines)))
            for line in lines:
                # 所有的列
                columns = line.contents
                if len(columns) < 7:
                    print('查询出经营风险-股权出质信息列不正确，共%d列' % len(columns))
                    continue
                try:
                    # 公示日期
                    date = columns[1].text
                    # 登记编号
                    registration_number = columns[2].text
                    # 出质人
                    pledgor = columns[3].text
                    # 质权人
                    pledgee = columns[4].text
                    # 状态
                    status = columns[5].text
                    # 出质股权数额
                    equity_amount = columns[6].text
                    stockRight = StockRight(date, registration_number, pledgor, pledgee, status, equity_amount)
                    stock_info = stockRight.__dict__
                    operating_risk_list.append(stock_info)
                except Exception as error:
                    print(error)
            current_num = param.pn + 1
            param.pn = current_num
            url = param.get_url_by_company_name()
            soup = get_soup(url=url, headers=headers)
    return operating_risk_list


if __name__ == '__main__':
    pagination_equity_base_url = 'https://www.tianyancha.com/pagination/equity.xhtml'
    company_name = '北京东方国信科技股份有限公司'
    param = Param(pagination_equity_base_url, company_id='', company_name=company_name, pn=1, ps=500)
    operating_risk_list = get_operating_risk(param)
    write_list_map_with_title(template_file_name, out_file_name, operating_risk_list, SEPARATION_CHARACTER, mode='a')
