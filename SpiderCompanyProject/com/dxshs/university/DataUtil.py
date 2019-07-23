import requests
import json
import threadpool
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

TOTAL = 1800
POOL_SIZE = 20
pool = ThreadPoolExecutor(POOL_SIZE)


def get_brief():
    """
    获取简介
    :return:
    """
    begin = time.time()
    print('查询概况开始...')
    url = 'https://gkcx.eol.cn/gkcx/api'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ''Chrome/51.0.2704.63 Safari/537.36'}
    param = {"uri": "gksjk/api/school/hotlists", "province_id": "", "type": "", "size": 200, "page": 1, "f211": "",
             "f985": "", "dual_class": "", "is_dual_class": "", "admissions": "", "central": "", "department": "",
             "school_type": "", "keyword": "", "request_type": 1, "sort": "view_total"}
    page = 0
    universities = []
    while len(universities) <= TOTAL:
        page += 1
        param['page'] = page
        html = requests.post(url, data=param, headers=headers).content
        content = json.loads(html)
        try:
            if 'data' in content:
                data = content['data']['item']
                if data:
                    universities.extend(data)
        except Exception as err:
            print(repr(str(err)))
        print('当前查询出记录条数：%d' % len(universities))
    if len(universities) > TOTAL:
        universities = universities[0:TOTAL]
    print('查询概况完成，查询记录条数：%d，耗时：%f秒' % (len(universities), (time.time() - begin)))
    return universities


def get_ids(universities):
    """
    获取id值
    :param universities:
    :return:
    """
    if universities:
        universities = list([university for university in universities if 'school_id' in university])
        return list(map(lambda university: university['school_id'], universities))
    return []


def get_detail(school_ids):
    """
    根据多个id查询详情
    :param school_ids:
    :return:
    """
    universities = []
    query_detail_begin = time.time()
    print('查询详情开始...')
    futures = [pool.submit(query_detail_by_id, id) for id in school_ids]
    for future in as_completed(futures):
        university = future.result()
        # print('多线程查询出详情：%s' % json.dumps(university))
        if university:
            universities.append(university)
    # requests = threadpool.makeRequests(query_detail_by_id, school_ids, callback)  # 创建要开启多线程的函数
    # [pool.putRequest(req) for req in requests]  # 将多线程的请求扔进线程池
    # pool.wait()

    # for id in school_ids:
    #     university = query_detail_by_id(id)
    #     if university:
    #         universities.append(university)
    print('查询详情结束，查询记录条数：%d,耗时：%f秒.' % (len(universities), (time.time() - query_detail_begin)))
    return universities


def query_detail_by_id(school_id):
    """
    根据id查详情
    :param school_id:
    :return:
    """
    if not school_id:
        print('school_id为空，数据查询失败！')
        return {}
    detail_url = 'https://gkcx.eol.cn/www/school/' + str(school_id) + '/info.json'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ''Chrome/51.0.2704.63 Safari/537.36'}
    html = requests.get(detail_url, headers=headers).content
    content = json.loads(html)
    return content


def conver_result(universities):
    """
    结果转换
    :param universities:
    :return:
    """
    result = []
    for university in universities:
        try:
            # 接入时间
            add_time = university['add_time']
            # 注册日期
            create_date = university['create_date']
            name = university['name']
            # 类型【理工类、综合类】
            type_name = university['type_name']
            belong = university['belong']
            # 机构代码
            code_enroll = university['code_enroll']
            # 地址
            address = university['address']
            # 联系电话
            phone = university['phone']
            # 简介
            text = university['content']
            # 邮编
            postcode = university['postcode']
            city_name = university['city_name']
            # 学校性质
            school_nature_name = university['school_nature_name']
            # 变更日期
            update_time = university['update_time']
            temp = {
                'jrsj': add_time,
                'zcrq': create_date,
                'jgdm': code_enroll,
                'jgmc': name,
                'jglx': type_name,
                'jyfw': school_nature_name,
                'jjhy': '教育',
                'xzqh': city_name,
                'jgdz': address,
                'zgjg': belong,
                'pzjg': belong,
                'dhhm': phone,
                'jj': text,
                'yzbm': postcode,
                'bgrq': update_time
            }
            result.append(temp)
        except Exception as err:
            print(repr(str(err)))
    return result


def loadTemplate():
    """
    读取模板文件
    :return:
    """
    with open('./universityTemplate.json', 'r') as file:
        return json.load(file)


def write_university(universities):
    template = loadTemplate()
    print('写文件开始...')
    flag = True
    head = []
    lines = []
    for university in universities:
        line = []
        for key in template:
            # 添加表头
            if flag:
                head.append(key + "（" + template[key] + "）")
            if key in university and university[key]:
                line.append(university[key])
            else:
                line.append('')
        if flag and head:
            lines.append('|'.join(head))
            flag = False
        line = list(map(lambda x: str(x), line))
        line = '|'.join(line)
        lines.append(line)
    write('./universityData.csv', lines, 'a')
    print('写文件完成.')


def write(file_name, lines, mode = 'a'):
    """
    写文件
    :param file_name: 文件名（包含路径）
    :param lines: 文本（列表）
    :param mode: 模式
    :return:
    """
    data = '\n'.join(lines)
    with open(file_name, mode) as file:
        file.write(data)


if __name__ == '__main__':
    universities = get_brief()
    ids = get_ids(universities)
    universities = get_detail(ids)
    universities = conver_result(universities)
    print('查询完成.')
    write_university(universities)
