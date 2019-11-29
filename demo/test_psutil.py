import psutil


def main():
    '''获取 chrome 浏览器进程的信息，官方介绍psutil：https://psutil.readthedocs.io/en/latest
    '''
    pids = [process.info['pid'] for process in psutil.process_iter(
        attrs=['pid', 'name']) if process.info['name'] == 'chrome.exe']
    cpu_percent = 0
    memory_percent = 0
    memory = 0
    total = psutil.virtual_memory().total
    used = psutil.virtual_memory().used
    for pid in pids:
        process = psutil.Process(pid)
        cpu_percent += process.cpu_percent()
        memory_percent += process.memory_percent(memtype='vms')
        memory += process.memory_info().vms
        print(pid, process.cpu_percent(), process.memory_percent(),
              process.memory_info().vms/1024)
    print('------统计------')
    print('浏览器 CPU 使用率：', cpu_percent)
    print('总 CPU 使用率：', psutil.cpu_percent())
    print('浏览器占用内存：', memory/1024)
    print('总占用内存：', used/1024)
    print('总内存：', total/1024)
    print('浏览器内存使用率：', memory_percent)
    print('浏览器内存使用率（计算）：', memory/total*100)
    print('总内存使用率：', psutil.virtual_memory().percent)
    print('总内存使用率（计算）：', used/total*100)


if __name__ == '__main__':
    main()
