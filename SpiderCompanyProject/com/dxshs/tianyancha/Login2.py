import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from seleniumrequests import Chrome

from com.dxshs.common.FileUtil import *

detail_url = 'https://www.tianyancha.com/company/11997559'

#企业关系基本url
relation_base_url = 'https://dis.tianyancha.com/dis/getInfoById/'


def login():
    driver = Chrome('/Users/liuxian/Downloads/chromedriver')
    driver.get("https://www.tianyancha.com/")
    driver.maximize_window()

    # 点击登录链接
    # loginLink = WebDriverWait(driver, 30).until(lambda x:x.find_element_by_xpath('//a[@onclick="header.loginLink(event)"]'))
    loginLink = WebDriverWait(driver, 30).until(lambda x: x.find_element_by_xpath('//a[text()="登录/注册"]'))
    print(loginLink.text)
    loginLink.click()

    # 切换到密码登录方式
    # login_by_pwd = WebDriverWait(driver, 30).until(lambda x:x.find_element_by_xpath('//div[@onclick="loginObj.changeCurrent(1);"]'))
    login_by_pwd = WebDriverWait(driver, 30).until(lambda x: x.find_element_by_xpath('//div[text()="密码登录"]'))
    print(login_by_pwd.text)
    login_by_pwd.click()

    # 输入用户名
    username = WebDriverWait(driver, 30).until(lambda x: x.find_elements_by_xpath('//input[@type="text"]')[4])
    username.send_keys('13926278814')
    # username.send_keys('13261731251')

    # 输入密码
    password = WebDriverWait(driver, 30).until(
        lambda x: x.find_element_by_css_selector('div.input-warp.-block > input.input.contactword'))
    password.send_keys('liubing0220')
    # password.send_keys('lx109718')

    # 取消登录保留一周的选项
    # saveoneweek = WebDriverWait(driver, 30).until(lambda x: x.find_element_by_css_selector('input.contactautoLogin'))
    # saveoneweek.click()

    # 点击登录按钮
    # login_button = WebDriverWait(driver, 30).until(lambda x:x.find_element_by_xpath('//div[@onclick="loginObj.loginByPhone(event);"]'))
    login_button = WebDriverWait(driver, 30).until(lambda x: x.find_element_by_xpath('//div[text()="登录"]'))
    print(login_button.text)
    driver.execute_script("arguments[0].click();", login_button)
    print('开始自动登录...')
    time.sleep(15)
    print('登录完成。')
    open(driver, detail_url)
    print('请手动通过验证码...')
    time.sleep(20)
    response = driver.request('GET', 'https://dis.tianyancha.com/dis/getInfoById/3027736699.json?')
    print(response)
    cookie = get_cookie(driver)
    return cookie
    # return driver


"""def login():
    driver = webdriver.Chrome('/Users/liuxian/Downloads/chromedriver')
    driver.get("https://www.tianyancha.com/")
    driver.maximize_window()

    # 点击登录链接
    # loginLink = WebDriverWait(driver, 30).until(lambda x:x.find_element_by_xpath('//a[@onclick="header.loginLink(event)"]'))
    loginLink = WebDriverWait(driver, 30).until(lambda x: x.find_element_by_xpath('//a[text()="登录/注册"]'))
    print(loginLink.text)
    loginLink.click()

    # 切换到密码登录方式
    # login_by_pwd = WebDriverWait(driver, 30).until(lambda x:x.find_element_by_xpath('//div[@onclick="loginObj.changeCurrent(1);"]'))
    login_by_pwd = WebDriverWait(driver, 30).until(lambda x: x.find_element_by_xpath('//div[text()="密码登录"]'))
    print(login_by_pwd.text)
    login_by_pwd.click()

    # 输入用户名
    username = WebDriverWait(driver, 30).until(lambda x: x.find_elements_by_xpath('//input[@type="text"]')[4])
    username.send_keys('13926278814')
    # username.send_keys('13261731251')

    # 输入密码
    password = WebDriverWait(driver, 30).until(
        lambda x: x.find_element_by_css_selector('div.input-warp.-block > input.input.contactword'))
    password.send_keys('liubing0220')
    # password.send_keys('lx109718')

    # 取消登录保留一周的选项
    # saveoneweek = WebDriverWait(driver, 30).until(lambda x: x.find_element_by_css_selector('input.contactautoLogin'))
    # saveoneweek.click()

    # 点击登录按钮
    # login_button = WebDriverWait(driver, 30).until(lambda x:x.find_element_by_xpath('//div[@onclick="loginObj.loginByPhone(event);"]'))
    login_button = WebDriverWait(driver, 30).until(lambda x: x.find_element_by_xpath('//div[text()="登录"]'))
    print(login_button.text)
    driver.execute_script("arguments[0].click();", login_button)
    print('开始自动登录...')
    time.sleep(20)
    print('登录完成。')
    return driver
    """

def get_cookie(driver):
    # driver = login()
    cookies = driver.get_cookies()
    data = []
    for cookie in cookies:
        name = cookie['name']
        value = cookie['value']
        temp = name + '=' + value
        data.append(temp)
    cookie = '; '.join(data)
    print('获取到的cookie值：%s' % cookie)
    return cookie


def open(driver, url):
    driver.get(url)
    driver.maximize_window()


# def open(url):
#     driver = webdriver.Chrome('/Users/liuxian/Downloads/chromedriver')
#     driver.get(url)
#     driver.maximize_window()
#     return get_cookie(driver)



if __name__ == '__main__':
    login()