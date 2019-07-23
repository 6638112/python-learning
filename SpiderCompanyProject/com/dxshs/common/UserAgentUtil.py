import random

from fake_useragent import UserAgent


def get_random_user_agent():
    """
    随机获取user-agent
    :return:
    """
    # 禁用服务器缓存
    # 出现异常(fake_useragent.errors.FakeUserAgentError: Maximum amount of retries reached), 可以禁用服务器缓存
    ua = UserAgent(use_cache_server=False)

    # 不缓存数据：
    # ua = UserAgent(cache=False)

    # 忽略ssl验证：
    # ua = UserAgent(verify_ssl=False)
    # 如果只想要某一个浏览器的，比如 Chrome ，那可以改成 ua.chrome，再次生成随机 UA 查看一下
    return ua.random


if __name__ == '__main__':
    for i in range(10):
        print(get_random_user_agent())
