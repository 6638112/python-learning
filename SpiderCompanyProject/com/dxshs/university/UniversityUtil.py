import requests
import json

LIMIT = 200


def get_university():
    """
    查询大学
    :return:
    """
    ranks = []
    url = 'http://www.gaokaopai.com/rank-index.html'
    # otype=2&city=0&cate=0&batch_type=2&start=125&amount=25
    params = {
        'otype': 2,
        'city': 0,
        'cate': 0,
        'batch_type': '',
        'start': 1,
        'amount': 25
    }
    head = {
        "Host": "sp0.baidu.com",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
        "Accept": "*/*",
        "Referer": "https://www.baidu.com/s?ie=utf-8&f=3&rsv_bp=1&tn=95943715_hao_pg&wd=%E8%80%81%E8%B5%96&oq=%25E8%2580%2581%25E8%25B5%2596&rsv_pq=ec5e631d0003d8eb&rsv_t=b295wWZB5DEWWt%2FICZvMsf2TZJVPmof2YpTR0MpCszb28dLtEQmdjyBEidZohtPIr%2FBmMrB3&rqlang=cn&rsv_enter=0&prefixsug=%25E8%2580%2581%25E8%25B5%2596&rsp=0&rsv_sug9=es_0_1&rsv_sug=9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8"
    }
    start = 1
    while len(ranks) <= LIMIT:
        start = len(ranks) + start
        if start > 1:
            start -= 1
        params['start'] = start
        html = requests.post(url, data=params).content
        if not html:
            break
        try:
            content = json.loads(html)
        except Exception as err:
            print(err)
        if 'data' in content:
            data = content.get('data')
            if 'ranks' in data:
                temp = data.get('ranks')
                ranks.extend(temp)

    return ranks

if __name__ == '__main__':
    ranks = get_university()
    names = []
    for university in ranks:
        name = university['uni_name']
        names.append(name)
    print(names)
    print('|'.join(names))
    with open('./university.csv', 'a') as file:
        file.write(",".join(names) + '\n')
    print('查询出学校：%d个' % len(ranks))
