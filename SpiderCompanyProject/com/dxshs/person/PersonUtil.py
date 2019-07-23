from com.dxshs.person.DishonestPersonUtil import *
from com.dxshs.util.RandomUtils import *

PAGE_LIMIT = 50

def generatePersonData():
    """
    生成person信息
    :return:
    """
    basePersons = get_dishonest_person(PAGE_LIMIT)
    basePersonSize = len(basePersons)
    print('查询出：%d条人员基本信息.' % basePersonSize)
    persons = []
    template = loadTemplate()
    templateStr = json.dumps(template, ensure_ascii=False)
    print('模板文件：', templateStr)
    for i in range(0, basePersonSize):
        person = {}
        basePerson = basePersons[i]
        idcard = get_idcard()
        sex = basePerson.sex
        age = get_age_by_idcard(idcard)
        phone = get_phone()
        qq = get_qq()
        education = get_degree_education()
        for key in template:
            if key == 'name':
                value = basePerson.name
            elif key == 'sex':
                value = basePerson.sex
            elif key == 'oldName':
                value = basePerson.name
            elif key == 'nation':
                value = get_nation()
            elif key == 'birthday':
                value = get_birthday_by_idcard(idcard)
            elif key == 'political_status':
                value = get_politic_countenance()
            elif key == 'card':
                value = idcard
            elif key == 'religious_belief':
                value = get_faith()
            elif key == 'speciality':
                value = get_skilled_in()
            elif key == '户主姓名':
                value = basePerson.name
            # elif key == 'spouse_name':
            #     '配偶姓名'
            elif key == 'tel':
                value = phone
            elif key == 'address':
                value = get_native_place()
            elif key == 'degree_education':
                value = education
            elif key == 'marital_status':
                value = get_marital_status(age)
            elif key == 'blood_type':
                value = get_blood_type()
            elif key == 'height':
                value = get_height()
            elif key == 'stamp':
                value = time.time()
            elif key == 'date':
                value = time.strftime("%Y-%m-%d", time.localtime(time.time()))
            elif key == 'age':
                value = age
            elif key == 'qq':
                value = qq
            elif key == 'idcard':
                value = idcard
            elif key == 'email':
                value = get_email(phone, qq)
            elif key == 'household':
                value = basePerson.areaName
            elif key == 'profession':
                value = get_profession()
            elif key == 'education':
                value = education
            elif key == 'nationality':
                value = '中国'
            elif key == 'qq_age':
                value = get_qq_age()
            elif key == 'password':
                value = get_password()
            elif key == 'data_source':
                value = '导入'
            elif 'date' in key:
                value = time.strftime('%Y%m%d', time.localtime(time.time()))
            else:
                value = ''
            person[key] = value
        persons.append(person)
    return persons

def loadTemplate():
    """
    读取模板文件
    :return:
    """
    with open('../person/personTemplate.json', 'r') as file:
        return json.load(file)

def writeFile(persons):
    print('写出用户信息至文件userInfo.csv开始...')
    with open('../person/userInfo.csv', 'w') as userFile:
        for person in persons:
            template = loadTemplate()
            line = []
            for key in template:
                line.append(person[key])
            line = list(map(lambda x : str(x), line))
            line = '|'.join(line)
            print(line)
            userFile.write(line + '\n')
    print('写文件完成.')

if __name__ == '__main__':
    persons = generatePersonData()
    writeFile(persons)
    print('构造出人员信息：%d条' % len(persons))