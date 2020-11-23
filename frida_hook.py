#coding=utf-8
import os
import time
import sys
import frida
import requests
import json

#打印javascript脚本返回消息
def on_message(message, data):
    if isinstance(message, dict):       
        data = toburp(message["payload"].encode('utf-8'))
        script.post(data) 
    else:
        if message.has_key("payload"):
            print(message["payload"])
#获取设备应用名
def get_application_name(device, identifier):
    for p in device.enumerate_applications():
        if p.identifier == identifier:
            return p.name
#获取设备进程pid
def get_process_pid(device, application_name):
    for p in device.enumerate_processes():
        if p.name == application_name:
            return p.pid
    return -1

def toburp(data):
    print(type(data))
    proxies = {'http':'http://127.0.0.1:8080'}
    url = 'http://127.0.0.1:8888/test'
    r=requests.post(url,data=data,proxies=proxies)
    return(r.text)

def main():
    #连接设备
    device = frida.get_device_manager().enumerate_devices()[-1]
    #需要attach的apk包名
    package_name = "com.*"
    #发现进程存活则杀死进程，等待进程重启
    pid = get_process_pid(device, package_name)
    if pid != -1:
        print("[+] killing {0}".format(pid))
        # device.kill(pid)
        time.sleep(0.3)
    while(1):
        pid = get_process_pid(device, package_name)
        if pid == -1:
            print("[-] {0} is not found...".format(package_name))
            time.sleep(2)
        else:
            break
    print("[+] Injecting script to {0}({1})".format(package_name, pid))
    session = None
    try:
        #attach目标进程
        session = frida.get_device_manager().enumerate_devices()[-1].attach(pid)
        #加载javaScript脚本
        script_content = open("hook.js").read()
        global script
        script = session.create_script(script_content)
        script.on("message", on_message)
        script.load()
        sys.stdin.read()
    except KeyboardInterrupt as e:
        if session is not None:
            session.detach()
            device.kill(pid)
        sys.exit(0)
if __name__ == "__main__":
    main()

