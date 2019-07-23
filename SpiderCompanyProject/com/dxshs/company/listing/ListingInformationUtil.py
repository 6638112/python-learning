# 发行相关
import os
from com.dxshs.common.CrawlerUtils import *
from com.dxshs.common.FileUtil import *

# url = 'https://www.tianyancha.com/company/3330019209'
url = 'https://www.tianyancha.com/company/11997559'
template_file_name = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '/templates/listingInfoTemplate.json'

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Host": "www.tianyancha.com",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "Cookie": "aliyungf_tc=AQAAANebsQWLswAAjIabJ/cMIq4ikFgO; csrfToken=CUlblbPZqr1cdp9Om2HeKm1d; TYCID=eef74250836811e9b3eb7fa713b59774; undefined=eef74250836811e9b3eb7fa713b59774; ssuid=4860560592; _ga=GA1.2.65095863.1559282237; bannerFlag=true; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1559284159,1559284270,1559286829,1559287410; _gid=GA1.2.1787049886.1559526377; token=b37f2d0862924836a77223fb3216fd8e; _utm=0cf78922917642c78561f71858a40858; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522signUp%2522%253A%25221%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E5%2588%2598%25E5%25BD%25BB%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522state%2522%253A%25220%2522%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522new%2522%253A%25221%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzI2MTczMTI1MSIsImlhdCI6MTU1OTU0MDQ5MCwiZXhwIjoxNTkxMDc2NDkwfQ.eYxGlYdscCrQINCrMcrnE-poJHqRo6EFKgnBSx-oSS0hva_i_3WDYmfJxyXndPeYGHnwOdEbFb5o5H4-4f0Pfw%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252213261731251%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzI2MTczMTI1MSIsImlhdCI6MTU1OTU0MDQ5MCwiZXhwIjoxNTkxMDc2NDkwfQ.eYxGlYdscCrQINCrMcrnE-poJHqRo6EFKgnBSx-oSS0hva_i_3WDYmfJxyXndPeYGHnwOdEbFb5o5H4-4f0Pfw; RTYCID=ec2e620e5031473bae28e0da732723c7; CT_TYCID=5c88023d78e34e65a8afc38945c001b4; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1559725807; cloud_token=62ba94a04ae24a17aa578c07be1065c0"
}


def get_listing_by_url(url, headers):
    soup = get_soup(url, headers)
    return get_listing_by_soup(soup)


def get_listing_by_soup(soup):
    """
    上市信息-发行相关
    :param soup:
    :return:
    """
    listing_info = {}
    issueRelated = soup.find_all(id='nav-main-issueRelatedNum')
    if issueRelated:
        contents = issueRelated[0].contents
        if len(contents) > 1:
            try:
                table = contents[1].contents[0]
                if table:
                    lines = table.contents[0].contents
                    for line in lines:
                        columns_per_line = line.contents
                        for i in range(len(columns_per_line)):
                            column = columns_per_line[i]
                            text = column.text
                            if not i % 2:
                                listing_info[text] = columns_per_line[i + 1].text
            except Exception as error:
                print(error)
    else:
        print('无上市信息！')
    listing_info = convert_by_template(template_file_name, listing_info)
    return listing_info

def convert_by_template(template_file_name, data):
    """
    根据模板转换文件
    :param template_file_name:
    :param data:
    :return:
    """
    convert_result = {}
    if data:
        template_file = read_json(template_file_name)
        for k,v in template_file.items():
            if v in data:
                convert_result[k] = data[v]
            else:
                convert_result[k] = ''
    return convert_result


if __name__ == '__main__':
    get_listing_by_url(url, headers)
