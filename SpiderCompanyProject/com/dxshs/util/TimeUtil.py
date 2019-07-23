import time

ticks = time.time()
print("当前时间戳：%s" % ticks)

localtime = time.localtime(ticks)
print("本地时间为：", localtime)

#asctime获取可读的时间模式的函数
localtime = time.asctime(localtime)
print("本地时间2为：", localtime)

#time.strftime(format[,t]
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print(time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()))

#将格式字符串转换为时间戳
a = "Sat Mar 28 22:24:24 2016"
print(time.mktime(time.strptime(a, "%a %b %d %H:%M:%S %Y")))

import calendar
cal = calendar.month(2019, 5)
print("打印日历：")
print(cal)
print(calendar.isleap(2019))