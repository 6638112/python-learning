# 企业关系
import requests

from com.dxshs.common.FileUtil import *

cookie = 'TYCID=eef74250836811e9b3eb7fa713b59774; undefined=eef74250836811e9b3eb7fa713b59774; ssuid=4860560592; _ga=GA1.2.65095863.1559282237; _gid=GA1.2.1787049886.1559526377; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522signUp%2522%253A%25221%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E5%2588%2598%25E5%25BD%25BB%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522state%2522%253A%25220%2522%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522new%2522%253A%25221%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzI2MTczMTI1MSIsImlhdCI6MTU1OTU0MDQ5MCwiZXhwIjoxNTkxMDc2NDkwfQ.eYxGlYdscCrQINCrMcrnE-poJHqRo6EFKgnBSx-oSS0hva_i_3WDYmfJxyXndPeYGHnwOdEbFb5o5H4-4f0Pfw%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252213261731251%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzI2MTczMTI1MSIsImlhdCI6MTU1OTU0MDQ5MCwiZXhwIjoxNTkxMDc2NDkwfQ.eYxGlYdscCrQINCrMcrnE-poJHqRo6EFKgnBSx-oSS0hva_i_3WDYmfJxyXndPeYGHnwOdEbFb5o5H4-4f0Pfw; RTYCID=ec2e620e5031473bae28e0da732723c7; CT_TYCID=5c88023d78e34e65a8afc38945c001b4; aliyungf_tc=AQAAAEOt01nwBwsAcz1F2qPBuJDhhYxl; bannerFlag=undefined; csrfToken=4mLlmFhJBiscqBaAtNldKtIx; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1559286829,1559287410,1559788597,1559788618; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1559788642; cloud_token=0cc70ba7528e45ba94488051c5731ac9; cloud_utm=be880a648c464dff82885af2424755df'
headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Host": "www.tianyancha.com",
    "Upgrade-Insecure-Requests": "1",
    "Referer": "https://dis.tianyancha.com/dis/old",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "Cookie": cookie
}


def get_business_relation(driver, base_url, company_id, headers, proxies):
    """
    查询企业关系
    :param driver:
    :param base_url:
    :param company_id:
    :param headers:
    :param proxies:
    :return:
    """
    url = base_url + str(company_id) + '.json'
    print('查询企业关系url：%s' % url)
    data = driver.get(url)
    if data:
        return relation_data_convert(data)
    return data


def get_business_relation_str(base_url, company_id, headers, proxies):
    """
    查询企业关系
    :param base_url:
    :param company_id:
    :return:
    """
    # url = base_url + str(company_id) + '.json'
    # print('查询企业关系url：%s' % url)
    # data = requests.get(url, headers=headers)
    # if data:
    #     return relation_data_convert(data)
    data = get_business_relation(base_url, company_id, headers, proxies)
    data = convert_to_str(data)
    return data


def relation_data_convert(result):
    """
    企业关系数据转换
    :param data:
    :return:
    """
    convert_result = {}
    print('开始进行企业关系结果转换...')
    data = result['data']
    nodes = data['nodes']
    relationships = data['relationships']
    # 数据封装
    nodeList, linkList = [], []  # 关系目标,关系描述
    # 关系分类
    legend = set()
    # 目标封装
    for node in nodes:
        temp = {}
        flag = str(node['labels'][0]) if node['labels'] else ""
        properties = node['properties']
        temp['category'] = properties['ntype']
        temp['name'] = properties['name']
        temp['value'] = 1
        if 'Company' == flag:
            temp['label'] = properties['name'] + "\n（主要）"
        nodeList.append(temp)

    for relationship in relationships:
        temp = {}
        startNode = relationship["startNode"];
        endNode = relationship["endNode"];
        labels = str(relationship['properties']['labels'][0]) if relationship['properties']['labels'] else ""
        legend.add(labels)
        temp['name'] = labels
        temp['weight'] = 1
        temp['source'] = ''
        temp['target'] = ''
        for node in nodes:
            id = node['id']
            if id == startNode:
                temp['target'] = node['properties']['name']
                continue
            elif id == endNode:
                temp['source'] = node['properties']['name']
                continue
        linkList.append(temp)
        convert_result['nodes'] = nodeList
        convert_result['links'] = linkList
        convert_result['legend'] = legend
    print('企业关系结果转换完成')
    return convert_result


def convert_to_str(result):
    return json.dumps(result, cls=MyEncoder, ensure_ascii=False)  # indent=4,


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        # if isinstance(obj, np.ndarray):
        #     return obj.tolist()
        if isinstance(obj, set):
            return list(obj)
        elif isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        else:
            return json.JSONEncoder.default(self, obj)


if __name__ == '__main__':
    url = 'https://dis.tianyancha.com/dis/getInfoById/'
    company_id = '11997559'
    # business_relation = get_business_relation(url, company_id)
    result = {}
    result = relation_data_convert(result)

    out_file_name = './businessRelationData.json'
    str_result = json.dumps(result, cls=MyEncoder, indent=4, ensure_ascii=False)
    write_str(out_file_name, str_result, mode='a')
