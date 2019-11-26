# 内置模块
from configparser import ConfigParser
from threading import Thread
from time import sleep
from datetime import datetime
import json
import os

# 第三方模块
from selenium import webdriver
import keyboard
import pyautogui
import psutil
import openpyxl

# 全局数据
g_config = None
g_driver = None
g_start_time = None
g_end_time = None
g_is_running = False
g_records = []


def operate_map():  # (1)操作地图

    # 生成初始缩放过程
    init_scrolls = []
    init_scrolls.extend([-1000 for i in range(8)])
    init_scrolls.extend([1000 for i in range(15)])

    # 生成拖动过程（顺时针螺旋形）
    screen_width, screen_height = pyautogui.size()  # 屏幕大小
    center_x, center_y = screen_width/2, screen_height/2
    drags = []
    direction = 'right'  # 拖动方向
    num = 0  # 方向上的拖动次数
    total = 50
    while total > 0:
        total -= 1
        if direction == 'right':  # 向右
            num = num+1
            drags.extend([{'direction': 'right', 'from': (center_x+300, center_y),
                           'to': (center_x-300, center_y)} for i in range(num)])
            direction = 'bottom'
        elif direction == 'bottom':  # 向下
            drags.extend([{'direction': 'bottom', 'from': (center_x, center_y+300),
                           'to': (center_x, center_y-300)} for i in range(num)])
            direction = 'left'
        elif direction == 'left':  # 向左
            num = num+1
            drags.extend([{'direction': 'left', 'from': (center_x-300, center_y),
                           'to': (center_x+300, center_y)} for i in range(num)])
            direction = 'top'
        elif direction == 'top':  # 向上
            drags.extend([{'direction': 'top', 'from': (center_x, center_y-300),
                           'to': (center_x, center_y+300)} for i in range(num)])
            direction = 'right'

    # 生成拖动时的缩放过程（缩-放-缩）
    scrolls = []
    scrolls.extend([-1000 for i in range(4)])
    scrolls.extend([1000 for i in range(6)])
    scrolls.extend([-1000 for i in range(2)])

    # 循环操作
    interval = float(g_config['interval'])
    while not is_stop():

        # 地图初始化
        script = 'd2cMap.setCenter([106.5590013579515, 29.55910442310595]);d2cMap.setZoom(12)'
        g_driver.execute_script(script)
        sleep(interval)

        # 鼠标缩放地图
        for init_scroll in init_scrolls:
            if is_stop():
                break
            pyautogui.moveTo(center_x, center_y)
            pyautogui.scroll(init_scroll)
            sleep(interval)

        # 鼠标拖动地图，并缩放地图
        drag_num = 0
        for drag in drags:
            if is_stop():
                break
            drag_num += 1
            pyautogui.moveTo(drag['from'][0], drag['from'][1])
            pyautogui.dragTo(drag['to'][0], drag['to']
                             [1], duration=0.2)
            sleep(interval)
            # 每拖动 3 下，进行缩放
            if drag_num == 3:
                drag_num = 0
                for scroll in scrolls:
                    if is_stop():
                        break
                    pyautogui.moveTo(center_x, center_y)
                    pyautogui.scroll(scroll)
                    sleep(interval)

    # 退出
    g_driver.close()
    g_driver.quit()


def record_data():  # (2)记录数据（每秒统计下 CPU 使用率、内存使用率、已用内存）
    interval = float(g_config['interval'])
    while g_is_running:
        time = datetime.now().strftime('%H:%M:%S')
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory().percent
        memory = psutil.virtual_memory().used
        record = {'time': time, 'cpu_percent': cpu_percent,
                  'memory_percent': memory_percent, 'memory': memory}
        g_records.append(record)
        sleep(interval)
    stat_data()


def stat_data():  # (3)统计数据
    xData = []
    yData_cpu = []
    yData_memory = []
    cpu_percent_sum = 0
    cpu_percent_avg = 0
    cpu_percent_over = 0
    memory_sum = 0
    memory_avg = 0
    memory_percent_sum = 0
    memory_percent_avg = 0
    memory_percent_over = 0
    for record in g_records:
        xData.append(record['time'])
        yData_cpu.append(record['cpu_percent'])
        yData_memory.append(record['memory_percent'])
        cpu_percent_sum = cpu_percent_sum+record['cpu_percent']
        memory_sum = memory_sum+record['memory']
        memory_percent_sum = memory_percent_sum+record['memory_percent']
        if record['cpu_percent'] >= 90:
            cpu_percent_over = cpu_percent_over+1
        if record['memory_percent'] >= 90:
            memory_percent_over = memory_percent_over+1
    length = len(g_records)
    cpu_percent_avg = cpu_percent_sum/length
    memory_avg = memory_sum/length
    memory_percent_avg = memory_percent_sum/length
    stat_info = f'（1）CPU 平均使用率：{float("%.2f" % cpu_percent_avg)}%；（2）CPU 使用率达 90% 及以上次数：{cpu_percent_over}；（3）内存平均使用率：{float("%.2f" % memory_percent_avg)}%；（4）内存使用用率达 90% 及以上次数：{memory_percent_over}；（5）内存平均使用大小：{int(memory_avg)}'
    save_to_excel(stat_info)
    save_to_json()
    save_to_chart(xData, yData_cpu, yData_memory, stat_info)
    print('------程序停止------')
    print('测试结果：', stat_info)


def save_to_excel(stat_info):  # (4)保存数据到 excel
    filename = g_config['excel']
    if os.path.isfile(filename):
        wb = openpyxl.load_workbook(filename)
    else:
        wb = openpyxl.Workbook()
    ws = wb.active
    now_col = 1 if ws.max_column in [0, 1] else ws.max_column+2
    ws.column_dimensions[openpyxl.utils.get_column_letter(now_col)].width = 20
    ws.column_dimensions[openpyxl.utils.get_column_letter(
        now_col+1)].width = 20
    ws.column_dimensions[openpyxl.utils.get_column_letter(
        now_col+2)].width = 20
    name_cell = ws.cell(row=1, column=now_col, value=g_config['name'])
    name_cell.font = openpyxl.styles.Font(bold=True)
    ws.merge_cells(start_row=1, start_column=now_col,
                   end_row=1, end_column=now_col+2)
    ws.cell(
        row=2, column=now_col).value = f'统计（{datetime.fromtimestamp(g_start_time)}至{datetime.fromtimestamp(g_end_time)}）：{stat_info}'
    ws.merge_cells(start_row=2, start_column=now_col,
                   end_row=2, end_column=now_col+2)
    ws.cell(row=3, column=now_col).value = 'CUP 使用率'
    ws.cell(row=3, column=now_col+1).value = '内存使用率'
    ws.cell(row=3, column=now_col+2).value = '已用内存'
    now_row = 4
    for record in g_records:
        ws.cell(row=now_row, column=now_col).value = record['cpu_percent']
        ws.cell(row=now_row, column=now_col +
                1).value = record['memory_percent']
        ws.cell(row=now_row, column=now_col +
                2).value = record['memory']
        now_row = now_row+1
    wb.save(filename=filename)


def save_to_json():  # (5)保存数据到 json 文件
    name = g_config['name']
    obj = {'title': name, 'records': g_records}
    with open(f'{name}.json', 'w') as f:
        f.write(json.dumps(obj))


def save_to_chart(xData, yData_cpu, yData_memory, stat_info):  # (6)保存到图表
    name = g_config['name']
    with open('conf/line_template.html', 'r', encoding='utf-8') as f:
        html = f.read()
        new_html = html.replace('{{title}}', name).replace(
            '{{text}}', name).replace('{{subtext}}', stat_info).replace('{{dataScript}}', f'''
    <script>
        var xData={json.dumps(xData)};
        var yData_cpu={json.dumps(yData_cpu)};
        var yData_memory={json.dumps(yData_memory)};
    </script>
        ''')
    with open(f'{name}.html', 'w', encoding='utf-8') as new_f:
        new_f.write(new_html)


def is_stop():  # (7)是否停止程序
    global g_end_time
    global g_is_running
    g_end_time = int(datetime.now().timestamp())
    time = int(g_config['minute'])*60
    if g_end_time-g_start_time > time:
        g_is_running = False
    return not g_is_running


def keyboard_listener():  # (8)快捷键监听，停止程序
    def stop():
        global g_is_running
        g_is_running = False
    keyboard.add_hotkey('ctrl+alt+s', stop)


def main():
    global g_config
    global g_driver
    global g_start_time
    global g_is_running

    # 读取配置信息
    config = ConfigParser()
    config.read('conf/config.ini', encoding="utf-8-sig")
    if not config.has_section('config'):
        print('------无正确配置信息，程序结束------')
        return
    g_config = config['config'] or {}

    # 驱动浏览器
    browser = g_config['browser'] or 'chrome'
    if browser == 'chrome':
        path = 'webdriver/chromedriver'
        g_driver = webdriver.Chrome(executable_path=path)
    elif browser == 'firefox':
        path = 'webdriver/geckodriver'
        g_driver = webdriver.Firefox(executable_path=path)
    elif browser == 'edge':
        path = 'webdriver/MicrosoftWebDriver.exe'
        g_driver = webdriver.Edge(executable_path=path)
    elif browser == 'ie':
        path = 'webdriver/IEDriverServer.exe'
        g_driver = webdriver.Ie(executable_path=path)
    elif browser == 'opera':
        path = 'webdriver/operadriver.exe'
        g_driver = webdriver.Opera(executable_path=path)
    g_driver.maximize_window()
    g_driver.get(g_config['url'])
    print('正在打开地图...')
    sleep(10)

    # 开启线程操作地图和记录数据
    print('------开始测试------')
    g_start_time = int(datetime.now().timestamp())
    g_is_running = True
    t1 = Thread(target=operate_map, name='operate_map')
    t2 = Thread(target=record_data, name='record_data')
    t3 = Thread(target=keyboard_listener, name='keyboard_listener')
    t1.start()
    t2.start()
    t3.start()


if __name__ == '__main__':
    main()
