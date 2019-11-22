# 内置模块
from time import sleep

# 第三方模块
from selenium import webdriver


def main(type):
    driver = None
    if type == 'chrome':
        driver = webdriver.Chrome('../webdriver/chromedriver.exe')
    elif type == 'firefox':
        driver = webdriver.Firefox('../webdriver/geckodriver.exe')
    elif type == 'edge':
        driver = webdriver.Edge('../webdriver/msedgedriver.exe')
    elif type == 'ie':
        driver = webdriver.Ie('../webdriver/IEDriverServer.exe')
    if driver:
        driver.get('https://www.baidu.com')
        driver.maximize_window()
        sleep(2)
    else:
        print('浏览器驱动不存在')


if __name__ == '__main__':
    main('ie')
