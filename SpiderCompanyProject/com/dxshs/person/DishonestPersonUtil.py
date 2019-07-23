import json

import requests

from com.dxshs.person.domain.BasePerson import *


def get_dishonest_person(total = 20):
    """
    查询失信人员信息
    :param total:
    :return:
    """
    persons = []
    for i in range(1, total + 1):
        print('正在抓取第' + str(i) + "页...")
        url = "https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6899&query=%E8%80%81%E8%B5%96&pn=" + str(
            i * 10) + "&ie=utf-8&oe=utf-8&format=json"
        head = {
            "Host": "sp0.baidu.com",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
            "Accept": "*/*",
            "Referer": "https://www.baidu.com/s?ie=utf-8&f=3&rsv_bp=1&tn=95943715_hao_pg&wd=%E8%80%81%E8%B5%96&oq=%25E8%2580%2581%25E8%25B5%2596&rsv_pq=ec5e631d0003d8eb&rsv_t=b295wWZB5DEWWt%2FICZvMsf2TZJVPmof2YpTR0MpCszb28dLtEQmdjyBEidZohtPIr%2FBmMrB3&rqlang=cn&rsv_enter=0&prefixsug=%25E8%2580%2581%25E8%25B5%2596&rsp=0&rsv_sug9=es_0_1&rsv_sug=9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.8"
        }
        html = requests.get(url, headers=head).content
        html_json = json.loads(html)
        html_data = html_json['data']
        for each in html_data:
            k = each['result']
            for each in k:
                name = each['iname']
                if '公司' in name:
                    continue
                sex = '男' if '男' in each['sexy'] else '女'
                idcard = each['cardNum']
                age = each['age']
                areaName = each['areaName']
                caseCode = each['caseCode']
                person = Person(name, sex, idcard, age, areaName, caseCode)
                # print(person.__dict__)
                persons.append(person)
    return persons

def write_to_file(persons):
    for person in persons:
        personStr = json.dumps(person.__dict__, ensure_ascii=False)
        with open('../person/file/dishonest_person.csv', 'a', encoding='utf-8') as file:
            file.write(personStr)

if __name__ == '__main__':
    persons = get_dishonest_person(10)
    write_to_file(persons)