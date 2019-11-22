# 内置模块
from time import sleep

# 第三方模块
from selenium import webdriver


def main(type):  # 官方说明：https://selenium.dev/documentation/en/webdriver/driver_requirements/
    driver = None
    if type == 'chrome':
        driver = webdriver.Chrome(executable_path='../webdriver/chromedriver')
    elif type == 'firefox':
        driver = webdriver.Firefox(executable_path='../webdriver/geckodriver')
    elif type == 'edge':
        driver = webdriver.Edge(
            executable_path='../webdriver/MicrosoftWebDriver.exe')
    elif type == 'ie':
        driver = webdriver.Ie(
            executable_path='../webdriver/IEDriverServer.exe')
    elif type == 'opera':
        driver = webdriver.Opera(
            executable_path='../webdriver/operadriver.exe')
    if driver:
        driver.get('https://www.baidu.com')
        driver.maximize_window()
        sleep(2)
    else:
        print('浏览器驱动不存在')


if __name__ == '__main__':
    main('chrome')
