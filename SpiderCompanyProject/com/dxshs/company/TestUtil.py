import json
import os

from com.dxshs.common.FileUtil import *

base_path = '../'

parent_path = os.path.abspath(os.path.dirname(os.getcwd())) + '/company'
company_data = parent_path + '/data/companyData.csv'
company_base_info_list = read_list(company_data)

company_columns = ['tel', 'email', 'site', 'brief', 'companyType', 'registrationNumber', 'registeredAddress',
           'registeredCapital', 'staffSize']


def set_value():
    data_file = './bonc.json'
    data = read_json(data_file)
    nodes = data.get('nodes')
    companies = [node for node in nodes if node.get('type') == 'Company']
    persons = [person for person in nodes if person.get('type') == 'Human']
    add_company_column(companies)
    add_person_column(persons)

    # company_names = []
    # company_file = parent_path + '/child_company_name_list.txt'
    # for company in companies:
    #     name = company.get('name')
    #     company_names.append(name)
    # write_by_line(company_file, company_names, 'w')

    # person_names = []
    person_file = parent_path + '/persons.txt'
    # for person in persons:
    #     name = person.get('name')
    #     person_names.append(name)
    # write_by_line(person_file, person_names, 'w')


    for company in companies:
        add_company_base_info(company)

    person_list = read_list(person_file)
    for person in persons:
        name = person.get('name')
        for person_info in person_list:
            if name in person_info and '|' in person_info:
                person['brief'] = person_info.split('|')[1]

    print('')

def add_company_column(companies):
    add_column(companies, company_columns)


def add_person_column(persons):
    columns = ['brief']
    add_column(persons, columns)


def add_column(list, columns):
    """
    添加列
    :param list:
    :param columns:
    :return:
    """
    for obj in list:
        for column in columns:
            obj[column] = ''


def add_company_base_info(company):
    """
    添加公司基本信息
    :param company:
    :return:
    """
    index = [2, 3, 4, 26, 13, 9, 24, 6, 19]
    company_name = company.get('name')
    for company_base_info in company_base_info_list:
        if company_name in company_base_info:
            base_info_columns = company_base_info.split('|')
            count = 0
            for column in company_columns:
                company[column] = base_info_columns[(index[count])]
                count += 1


def set_person_base_info(person):

    return ''


if __name__ == '__main__':
    set_value()
