import random
import time
import datetime
from com.dxshs.util.IdcardUtil import *


def generateSex():
    sex = ['男', '女']
    return random.choice(sex)


def random_by_weight(weight_data):
    total = sum(weight_data.values())  # 权重求和
    ra = random.uniform(0, total)  # 在0与权重和之前获取一个随机数
    curr_sum = 0
    ret = None
    # keys = weight_data.iterkeys()    # 使用Python2.x中的iterkeys
    keys = weight_data.keys()  # 使用Python3.x中的keys
    for k in keys:
        curr_sum += weight_data[k]  # 在遍历中，累加当前权重值
        if ra <= curr_sum:  # 当随机数<=当前权重和时，返回权重key
            ret = k
            break
    return ret


def get_nation():
    # nations = ["汉族", "壮族", "满族", "回族", "苗族", "维吾尔族","土家族", "彝族", "蒙古族", "藏族", "布依族", "侗族","瑶族", "朝鲜族", "白族", "哈尼族", "哈萨克族", "黎族", "傣族"]
    nation_map = {
        "汉族": 55, "壮族": 1, "满族": 1, "回族": 1, "苗族": 1, "维吾尔族": 1, "土家族": 1, "彝族": 1, "蒙古族": 1, "藏族": 1, "布依族": 1,
        "侗族": 1, "瑶族": 1, "朝鲜族": 1, "白族": 1, "哈尼族": 1, "哈萨克族": 1, "黎族": 1, "傣族": 1
    }
    return random_by_weight(nation_map)


def get_idcard():
    return getRandomIdcard()


def get_birthday_by_idcard(idcard):
    idcard = str(idcard)
    birthday = idcard[6:14]
    timeStruct = time.strptime(birthday, "%Y%m%d")
    return time.strftime("%Y-%m-%d", timeStruct)


def get_age_by_idcard(idcard):
    """
    获取年龄
    :param idcard:
    :return:
    """
    idcard = str(idcard)
    birth_year = idcard[6:10]
    now = datetime.now()
    year = now.year
    age = int(year) - int(birth_year)
    return age


def get_politic_countenance():
    """
    政治面貌
    :return:
    """
    politic = {'群众': 90, '党员': 10, '团员': 1}
    return random_by_weight(politic)


def get_faith():
    """
    宗教信仰
    :return:
    """
    faith = ['基督教', '伊斯兰教', '佛教', '道教']
    return random.choice(faith)


def get_skilled_in():
    """
    特长
    :return:
    """
    skilled_in = ["跑步", "高尔夫", "羽毛球", "游泳", "乒乓球", "冰球", "篮球", "旱冰", "街舞", "民族舞", "芭蕾舞", "桑巴舞", "提琴", "笛", "琵琶", "古筝",
                  "美声", "通俗流行声乐", "素描", "速写", "油画", "书法", "水彩画", "水粉画", "陶艺", "手工艺", "摄影", "插花", "茶艺", "剪纸",
                  "小品主持", "文案写作"]
    return random.choice(skilled_in)


def get_phone():
    """
    手机号
    :return:
    """
    # 第二位数字
    second = [3, 4, 5, 7, 8][random.randint(0, 4)]

    # 第三位数字
    third = {
        3: random.randint(0, 9),
        4: [5, 7, 9][random.randint(0, 2)],
        5: [i for i in range(10) if i != 4][random.randint(0, 8)],
        7: [i for i in range(10) if i not in [4, 9]][random.randint(0, 7)],
        8: random.randint(0, 9),
    }[second]

    # 最后八位数字
    suffix = random.randint(9999999, 100000000)

    # 拼接手机号
    return "1{}{}{}".format(second, third, suffix)


def get_native_place():
    """
    籍贯
    :return:
    """
    province = ["北京", "天津", "上海", "重庆", "河北", "山西", "辽宁", "吉林", "黑龙江", "江苏", "浙江", "安徽", "福建", "江西", "山东", "河南", "湖北",
                "湖南", "广东", "海南", "四川", "贵州", "云南", "陕西", "甘肃", "青海", "台湾", "内蒙古", "广西壮族自治区", "西藏", "宁夏回族自治区", "新疆",
                "香港", "澳门"]
    return random.choice(province)


def get_degree_education():
    """
    文化程度
    :return:
    """
    # education = {"博士": 2, "硕士": 2, "本科": 10, "大专": 20, "中专和中技": 10, "技工学校": 5, "高中": 30, "初中": 30, "小学": 40,
    #              "文盲与半文盲": 50}
    education = {"博士": 2, "硕士": 5, "本科": 50, "大专": 20, "高中": 10}
    return random_by_weight(education)


def get_marital_status(age=18):
    """
    婚姻状况
    :return:
    """
    return '已婚' if int(age) >= 30 else '未婚'


def get_blood_type():
    """
    血型
    :return:
    """
    blood = {'O': 7, 'A': 1, 'B': 1, 'AB': 1}
    return random_by_weight(blood)


def get_height():
    """
    身高
    :return:
    """
    return random.randint(155, 184)


def get_qq():
    """
    qq
    :return:
    """
    qq = [random.randint(1, 9)] + [random.randint(0, 10) for _ in range(8)]
    qq = list(map(lambda x: str(x), qq))
    return ''.join(qq)


def get_email(phone, qq):
    """
    邮箱
    :return:
    """
    suffix = ["163.com", "126.com"]
    at = '@'
    phone = str(phone).strip()
    qq = str(qq).strip()
    mail = [phone + at + random.choice(suffix), qq + at + 'qq.com']
    return random.choice(mail)


def get_weibo():
    return ''


def get_profession():
    profession = ["作业员", "技术员", "工程师", "设计师", "管理员", "总务人员", "厨师", "服务员", "营销人员", "保安", "司机", "导游", "售票员", "调酒师", "营业员",
                  "促销", "保姆", "医生", "护士", "药剂师", "营养师", "后勤", "健身教练", "按摩技师", "演员", "导演", "制片", "经纪", "编剧", "场务", "音乐人",
                  "歌手", "乐师", "车手", "经纪", "分析师", "服务员", "会记", "银行柜台", "保险销售", "教师", "培训师", "教练", "咨询师", "运动员", "陪练",
                  "教练", "裁判", "公务员", "警察", "军人", "特工", "科研人员", "记者", "摄影", "航天员", "会记", "人事", "保安", "总台", "翻译"];
    return random.choice(profession)


def get_qq_age():
    return random.randint(2, 5)

def get_password():
    """
    邮箱密码
    :return:
    """
    return ''.join(random.sample('abcdefghijklmnopqrstuvwxyz0123456789', random.randint(6, 10)))

if __name__ == '__main__':
    weight_data = {'a': 1, 'b': 1, 'c': 8}
    for i in range(10):
        # print(get_email(phone='13261731251',qq='1805475005'))
        print(get_password())
        # print('%s,身高:%d,年龄:%s' % (get_degree_education(), get_height(), get_age_by_idcard('420607199309063613')))
        # print('%s' % random_by_weight(weight_data))
