import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from com.dxshs.common.FileUtil import *
url = 'https://www.tianyancha.com/company/11997559'


def open_url(url = url):
    driver = webdriver.Chrome('/Users/liuxian/Downloads/chromedriver')
    driver.get(url)
    driver.maximize_window()


if __name__ == '__main__':
    open_url()