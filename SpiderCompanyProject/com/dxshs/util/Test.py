import requests
import json
from com.dxshs.util.IdcardUtil import *
from com.dxshs.util.PhoneUtil import *
from com.dxshs.util.NationUtil import *

num = 0
user_all=[]
MAX = 20
#title = ['name', 'gender', 'oldName', 'nation', 'birthday', 'political_status', 'card', 'locations', 'business' ,'school', 'major', 'company', 'job'];
title = ['name','sex','oldName', 'nation', 'birthday', 'political_status', 'card', 'tel', 'address']

#查询url数据
def get_url(url):
    header_info = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    }
    user_url = url
    response = requests.get(user_url, headers=header_info)
    data = response.content
    data = data.decode('utf-8')  # 设置字符集
    return data

#获取关注列表
def get_follower(userId):             #解析内容，获取关注用户
    list=[]
    url = 'https://www.zhihu.com/api/v4/members/'+userId+'/followees?' \
          'include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%' \
          '2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=200'
    data = get_url(url)
    data = json.loads(data)['data']
    print(data)
    for user in data:
        list.append(user['url_token'])
    return list

def digui(list):
    global num  # 全局变量，爬取多少次
    temporary = []  # 存放本次爬取的用户名
    for url in list:
        if (num == MAX):
            return 0
        else:
            num = num + 1
            print(num)
            list = get_follower(url)
            user_all.extend(list)  # 全局变量，存放所有爬取的用户名
            temporary.extend(list)  # 存放本次爬取的用户名
            print(list)
    digui(temporary)  # 递归爬取

def get_user_info(userID):
    info=[]
    url="https://www.zhihu.com/api/v4/members/"+userID+"?include=locations%2Cemployments%2Cgender%2Ceducations%2Cbusiness%2Cvoteup_count%2Cthanked_Count%2Cfollower_count%2Cfollowing_count%2Ccover_url%2Cfollowing_topic_count%2Cfollowing_question_count%2Cfollowing_favlists_count%2Cfollowing_columns_count%2Cavatar_hue%2Canswer_count%2Carticles_count%2Cpins_count%2Cquestion_count%2Ccolumns_count%2Ccommercial_question_count%2Cfavorite_count%2Cfavorited_count%2Clogs_count%2Cmarked_answers_count%2Cmarked_answers_text%2Cmessage_thread_token%2Caccount_status%2Cis_active%2Cis_bind_phone%2Cis_force_renamed%2Cis_bind_sina%2Cis_privacy_protected%2Csina_weibo_url%2Csina_weibo_name%2Cshow_sina_weibo%2Cis_blocking%2Cis_blocked%2Cis_following%2Cis_followed%2Cmutual_followees_count%2Cvote_to_count%2Cvote_from_count%2Cthank_to_count%2Cthank_from_count%2Cthanked_count%2Cdescription%2Chosted_live_count%2Cparticipated_live_count%2Callow_message%2Cindustry_category%2Corg_name%2Corg_homepage%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics"
    data=get_url(url)
    print("查询出用户信息如下：%s", data)
    data = json.loads(data)


    # if 'avatar_url' in data:
    #     info.append(data['avatar_url'])       #头像
    # else:
    #     info.append('')
    # if 'url_token' in data:
    #     info.append(data['url_token'])  # id
    # else:
    #     info.append('')

    if 'name' in data:
        name = data['name']
    else:
        name = '张三'
    info.append(name)
    if 'gender' in data:
        info.append(getGender(data['gender']))  # 性别
    else:
        info.append('男')
    #曾用名
    info.append(name)
    #民族
    info.append(getRandomNation())
    idcard = getRandomIdcard()
    #出生日期
    info.append(getBirthdayFromIdcard(idcard))
    #政治面貌
    info.append(random.choice(['群众', '党员', '团员']))
    #证件号
    info.append(idcard)
    #手机号
    info.append(createRandomPhone())
    try:
        if 'name' in data['locations'][0]:
            info.append(data['locations'][0]['name'])  # 居住地
        else:
            info.append('')
    except:
        info.append('')

    # if 'business' in data:
    #     info.append(data['business']['name'])  # 所在行业
    # else:
    #     info.append('')
    # try:
    #     if "school" in data['educations'][0]:
    #         info.append(data['educations'][0]['school']['name'])  # 学校
    #     else:
    #         info.append('')
    # except:
    #     info.append('')
    # try:
    #     if 'major' in data['educations'][0]:
    #         info.append(data['educations'][0]['major']['name'])      #专业
    #     else:
    #         info.append('')
    # except:
    #     info.append('')
    # if 'follower_count' in data:
    #     info.append(data['follower_count'])  # 粉丝
    # else:
    #     info.append('')
    # if 'following_count' in data:
    #     info.append(data['following_count'])  # 关注
    # else:
    #     info.append('')
    # if 'voteup_count' in data:
    #     info.append(data['voteup_count'])  # 获赞
    # else:
    #     info.append('')
    # if 'thanked_count' in data:
    #     info.append(data['thanked_count'])  # 感谢
    # else:
    #     info.append('')
    # if 'favorited_count' in data:
    #     info.append(data['favorited_count'])  # 收藏
    # else:
    #     info.append('')
    # if 'answer_count' in data:
    #     info.append(data['answer_count'])  # 回答数
    # else:
    #     info.append('')
    # if 'following_question_count' in data:
    #     info.append(data['following_question_count'])  # 关注的问题
    # else:
    #     info.append('')
    # try:
    #     if 'company' in data['employments'][0]:
    #         info.append(data['employments'][0]["company"]['name'])  # 公司
    #     else:
    #         info.append('')
    # except:
    #     info.append('')
    #
    # try:
    #     if 'job' in data['employments'][0]:
    #         info.append(data['employments'][0]["job"]['name'])  # 职位
    #     else:
    #         info.append('')
    # except:
    #     info.append('')

    return info

def getGender(genderCode) :
    return '男' if genderCode == 1 else '女'

import time
import random
a1=(1976,1,1,0,0,0,0,0,0)              #设置开始日期时间元组（1976-01-01 00：00：00）
a2=(2019,5,1,23,59,59,0,0,0)    #设置结束日期时间元组（1990-12-31 23：59：59）
start=time.mktime(a1)    #生成开始时间戳
end=time.mktime(a2)      #生成结束时间戳

def getRandomBirthday():
    """
    随机生成出生日期
    :return:
    """
    t = random.randint(start, end)  # 在开始和结束时间戳中随机取出一个
    date_touple = time.localtime(t)  # 将时间戳生成时间元组
    date = time.strftime("%Y-%m-%d", date_touple)  # 将时间元组转成格式化字符串（1976-05-21）
    print(date)

def getBirthdayFromIdcard(idcard):
    birthday = idcard[6:14]
    timeStruct = time.strptime(birthday, "%Y%m%d")
    return time.strftime("%Y-%m-%d", timeStruct)

if __name__ == '__main__':
    with open('./url.txt', 'r') as f:
        lines = f.readlines()  # 读取所有行
        last_line = lines[-1]  # 取最后一行
    user_id = last_line  # 继续上一次的爬取
    user = get_follower(user_id)
    if (user == None):
        print("没有关注的人")
    else:
        digui(user)
    user_all = list(set(user_all))  # 去掉重复的用户重
    f = open('./url.txt', 'a')  # 写入文本文件
    for text in user_all:
        f.write('\n' + text)
    user_list = user_all
    f.close()

    with open('../person/userInfo.csv', 'a') as userFile:
        userFile.write('|'.join(title) + '\n')
        for id in user_list:
            user_id = id
            info = get_user_info(user_id)
            info = [str(i) for i in info]  # 转为字符串
            info = '|'.join(info)
            print(info)
            userFile.write(info + '\n')
    userFile.close()
