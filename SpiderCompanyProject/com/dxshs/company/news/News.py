# 新闻舆情

import os

from com.dxshs.common.CrawlerUtils import *
from com.dxshs.common.FileUtil import *
from com.dxshs.common.Param import Param

template_file_name = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '/templates/newsInfoTemplate.json'
out_file_name = './newsData.csv'
# 分隔符
SEPARATION_CHARACTER = '|`|'

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
TYPE_MESSAGE = '新闻舆情'


class News(object):
    __doc__ = '新闻舆情'

    def __init__(self, bt, nr, ly, rq, xq):
        self.bt = bt
        self.nr = nr
        self.ly = ly
        self.rq = rq
        self.xq = xq


def get_news(param, headers=headers):
    """
    新闻舆情
    :param param:
    :param headers:
    :return:
    """
    result = []
    url = param.get_url_by_company_id()
    soup = get_soup(url=url, headers=headers)
    if not soup:
        print(('url：%s查询出' + TYPE_MESSAGE + '信息为空') % url)
        return result
    while soup:
        try:
            # 所有的行
            lines = soup.find(class_='company-news-container').contents
        except Exception as error:
            break
        if not lines:
            break
        print(('url：%s，查询出' + TYPE_MESSAGE + '信息记录条数：%s条') % (url, len(lines)))
        for line in lines:
            # 所有的列
            columns = line.contents
            if len(columns) < 3:
                print(('查询出' + TYPE_MESSAGE + '信息列不正确，共%d列') % len(columns))
                continue
            try:
                # 标题
                title = columns[0].text.replace('\t', '').replace(' ', '')
                # 详情
                detail = columns[0].contents[0].attrs['href']
                # 内容
                content = columns[1].text
                # 来源
                source = columns[2].contents[0].text.replace('来源：', '').replace('来源', '')
                # 日期
                date = columns[2].contents[1].text
                news = News(title, content, source, date, detail)
                news_map = news.__dict__
                result.append(news_map)
            except Exception as error:
                print(error)
        current_num = param.pn + 1
        param.pn = current_num
        url = param.get_url_by_company_id()
        soup = get_soup(url=url, headers=headers)
    return result


if __name__ == '__main__':
    news_base_url = 'https://www.tianyancha.com/pagination/findNewsCount.xhtml'
    company_id = '11997559'
    company_name = '北京东方国信科技股份有限公司'
    param = Param(news_base_url, company_id, company_name=company_name, pn=1, ps=100)
    news_list = get_news(param)
    write_list_map_with_title(template_file_name, out_file_name, news_list, SEPARATION_CHARACTER,
                              mode='a')
