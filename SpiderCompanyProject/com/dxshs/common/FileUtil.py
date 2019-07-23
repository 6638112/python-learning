import json
import os


def read_json(file_name):
    """
    读取文件
    :param file_name:
    :return:
    """
    with open(file_name, 'r') as file:
        return json.load(file)


def read_list(file_name):
    lines = []
    with open(file_name, 'r') as file:
        for line in file:
            line = line.strip('\n')
            lines.append(line)
    return lines


def write_by_line(file_name, lines, mode='a'):
    """
    写文件
    :param file_name: 文件名（包含路径）
    :param lines: 文本（列表）
    :param mode: 模式
    :return:
    """
    print('写文件开始...')
    if len(lines) > 1:
        data = '\n'.join(lines)
    elif len(lines) == 1:
        data = lines[0] + '\n'
    else:
        print('内容为空，未执行写文件操作！')
        return
    path = '/'.join(file_name.split('/')[0:-1])
    if not is_exist(path):
        makedir(path)
    if not is_exist(file_name):
        create_file(file_name)
    with open(file_name, mode) as file:
        file.write(data)
    print('写文件完成.')


def write_list_map_with_title(template_file_name, out_file_name, data, separation_character, mode='a'):
    """
    写文件
    :param template_file_name: 模板文件
    :param out_file_name: 输出文件
    :param data: 数据（list[map]）
    :param separation_character: 分隔符
    :param mode: 写文件模式
    :return:
    """
    # 读取模板文件
    template_file = read_json(template_file_name)
    title = get_title(template_file, separation_character)
    contents = get_content(template_file, data, separation_character)
    lines = []
    lines.append(title)
    lines.extend(contents)
    # 写文件
    write_by_line(out_file_name, lines, mode)


def write_list_map_without_title(template_file_name, out_file_name, data, separation_character, mode='a'):
    """
    写文件
    :param template_file_name: 模板文件
    :param out_file_name: 输出文件
    :param data: 数据（list[map]）
    :param separation_character: 分隔符
    :param mode: 写文件模式
    :return:
    """
    # 读取模板文件
    template_file = read_json(template_file_name)
    lines = get_content(template_file, data, separation_character)
    # 写文件
    write_by_line(out_file_name, lines, mode)


def get_content(template_file, data, separation_character):
    """
    获取内容行
    :param template_file_name: 模板文件
    :param data: 数据
    :param separation_character:分隔符
    :return:
    """
    lines = []
    keys = list(template_file.keys())
    for map in data:
        columns = []
        for k in keys:
            if k in map:
                v = map[k]
            else:
                v = ''
            columns.append(v)
        line = separation_character.join(columns)
        lines.append(line)
    return lines


def get_title(template_file, separation_character):
    """
    获取标题
    :param template_file_name: 模板文件
    :param separation_character: 分隔符
    :return:
    """
    keys = template_file.keys()
    title = separation_character.join(keys)
    return title


def write_json_list(file_name, data, mode='a'):
    """
    写出json文件
    :param file_name:
    :param data:
    :param mode:
    :return:
    """
    with open(file_name, mode=mode) as file:
        json.dump(data, file)

def write_str(file_name, data, mode='a'):
    """
    写字符串
    :param file_name:
    :param data:
    :param mode:
    :return:
    """
    with open(file_name, mode=mode, encoding='utf-8') as file:
        file.write(data)


def write_json_with_title(template_file_name, out_file_name, data, separation_character, mode='a'):
    """
    通过json数据写csv文件
    :param template_file_name:
    :param out_file_name:
    :param data:
    :param separation_character:
    :param mode:
    :return:
    """
    # 读取模板文件
    template_file = read_json(template_file_name)
    title = get_title(template_file, separation_character)
    content = []
    for k in template_file.keys():
        if k in data:
            content.append(data[k])
        else:
            content.append('')
    content = separation_character.join(content)
    lines = []
    lines.append(title)
    lines.append(content)
    # 写文件
    write_by_line(out_file_name, lines, mode)


def write_json_without_title(template_file_name, out_file_name, data, separation_character, mode='a'):
    """
    通过json数据写csv文件
    :param template_file_name:
    :param out_file_name:
    :param data:
    :param separation_character:
    :param mode:
    :return:
    """
    content = []
    template_file = read_json(template_file_name)
    for k in template_file.keys():
        if k in data:
            content.append(data[k])
        else:
            content.append('')
    content = separation_character.join(content)
    lines = []
    lines.append(content)
    # 写文件
    write_by_line(out_file_name, lines, mode)


def is_exist(path):
    return os.path.exists(path)


def makedir(path):
    os.makedirs(path)

def create_file(path):
    """
    创建文件
    :param path:
    :return:
    """
    os.system(r"touch {}".format(path))  # 调用系统命令行来创建文件