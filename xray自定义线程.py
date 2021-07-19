# -*- coding: utf-8 -*-
# 用法： 在的同目录下生成xray_url.txt，根据自己的需求更改scan_command即可
# 环境： python3
# 说明： command中的xray路径需要手动修改，报告生成的位置在同一目录下
import os
import hashlib
import re
import queue
import threading
import sys


def main(threadNum):
    # 以队列的形式获取要扫描的url
    url_queue = get_url(file="xray_url.txt")
    # 利用多线程进行xray扫描
    threads = []
    for i in range(threadNum):
        t = threading.Thread(target=xray, args=(url_queue, ))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()


# 定义url获取函数get_url()
def get_url(file="xray_url.txt"):
    url_queue = queue.Queue()
    f = open(file, "r", encoding="gbk")
    for i in f.readlines():
        url = i.strip()
        url_queue.put(url)
    f.close()
    return url_queue


# 定义xray扫描函数
def xray(url_queue):
    while not url_queue.empty():
        line = url_queue.get()
        # 匹配http | https请求头
        pattern = re.compile(r'^(https|http)://')
        try:
            if not pattern.match(line.strip()):
                targeturl = "http://" + line.strip()
            else:
                targeturl = line.strip()
            outputfilename = hashlib.md5(targeturl.encode("utf-8"))
            do_scan(targeturl.strip(), outputfilename.hexdigest())
        except Exception as e:
            print(e)
            pass
    else:
        print("Xray Scan End~")
        sys.exit()


# 报告
def do_scan(targeturl, outputfilename="test"):
    scan_command = "E:\XRAY1.7.1/xray.exe webscan --browser-crawler {} --html-output {}.html".format(targeturl, outputfilename)
    os.system(scan_command)
    return


if __name__ == '__main__':
    threadNum = int(input("Please input threads:"))
    main(threadNum)
