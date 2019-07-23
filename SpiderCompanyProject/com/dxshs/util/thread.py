import _thread
import time

class ThreadTest(object):
    @staticmethod
    def print_time(threadName, delay):
        count = 0
        while count < 5:
            time.sleep(delay)
            count += 1
            print("%s:%s" % (threadName, time.ctime(time.time())))


    @staticmethod
    def newThreads():
        try:
            _thread.start_new_thread(ThreadTest.print_time("thread-1", 2))
            _thread.start_new_thread(ThreadTest.print_time("thread-2", 4))
        except:
            print("error:无法启动线程")

if __name__ == '__main__':
    ThreadTest.newThreads()