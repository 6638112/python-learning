import random

all_nations = ["汉族","壮族","满族","回族","苗族","维吾尔族",
"土家族","彝族","蒙古族","藏族","布依族","侗族",
"瑶族","朝鲜族","白族","哈尼族","哈萨克族","黎族"]
def getRandomNation():
    return random.choice(all_nations)