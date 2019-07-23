import threading
import time

existFlag = 0

class MyThread(threading.Thread):
    def __init__(self, threadId, name, counter):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.name = name
        self.counter = counter

    def run(self):
        print("开始线程：" + self.name)
        print_time(self.name, self.counter, 5)
        print("退出线程：" + self.name)


def print_time(threadName, delay, counter):
    while counter:
        if existFlag:
            threadName.exit()
        time.sleep(delay)
        #Python time ctime() 函数把一个时间戳（按秒计算的浮点数）转化为time.asctime()的形式
        print("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1

thread1 = MyThread(1, "thread1", 1)
thread1.start()