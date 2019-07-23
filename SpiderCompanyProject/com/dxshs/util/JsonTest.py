import json

class Test:
    def read(self):
        data = {
            "beginTime":"20190101000000",
            "endTime":"20190429235959",
            "idType":"msisdn",
            "sourceSet":"13261731251"
        }
        #对数据进行编码 将python字典类型转换为json对象
        json_str = json.dumps(data)
        print("python原始数据：", repr(data))
        print("json对象：%s, %s" % (type(json_str), json_str))

        #json.loads()对数据进行解码 将json对象转换为python字典
        data2 = json.loads(json_str)
        print("beginTime:%s, %s" % (type(data2), data2['beginTime']))

        #写入json数据
        with open('data.json', 'w') as f:
            json.dump(data, f)
        f.close()

        #读取数据
        with open('data.json', 'r') as f:
            data = json.load(f)
            print("type:%s, data:%s" % (type(data), data))

if __name__ == '__main__':
    Test().read()