"""
广播模块
每天复读机,复读每日消息
包含图片，新闻，天气等等
"""
from wxpy import *
import threading
import time
import constant
import os
import pyweathercn
import random


global isRepeat
isRepeat = constant.isRepeat


class Broadcast:
    __text = []
    __img = []

    def __init__(self, text, img):
        self.__text = text
        self.__img = img

    def append(self, text):
        self.__text.append(text)

    def send_broadcast(self):
        for value in constant.deliver_list.values():
            value.send('\n'.join(self.__text))
            #for img_path in self.__img:
               # print(img_path)
               #value.send_image('%s' % img_path)


def start_repeat(broadcast=None, second=0, minute=0, hour=0, day=0):
    """
    向广播列表中间隔发送广播
    :param broadcast: 广播消息，消息内容不变
    :param second: 间隔秒
    :param minute: 间隔分钟
    :param hour: 间隔小时
    :param day: 间隔天
    :return:
    """
    broadcast.send_broadcast()
    global isRepeat
    if isRepeat:
        threading.Timer(second + minute * 60 + hour * 3600 + day * 86400, start_repeat,
                    [broadcast, second, minute, hour, day]).start()


def stop_repeat():
    global isRepeat
    isRepeat = False


def module_broadcast(text=False, img=False, second=0, minute=0, hour=0, day=0):
    try:
        threading.Thread(target=module_repeat, args=[text, img, second, minute, hour, day]).start()
    except Exception:
        constant.bot.file_helper.send('启动失败')


def module_repeat(text=False, img=False, second=0, minute=0, hour=0, day=0):
    msg = []
    imsg = []
    if text:
        t = ''
        if time.localtime(time.time()).tm_hour < 6:
            t = t + '凌晨好'
        elif time.localtime(time.time()).tm_hour < 8:
            t = t + '早上好'
        elif time.localtime(time.time()).tm_hour < 12:
            t = t + '上午好'
        elif time.localtime(time.time()).tm_hour < 13:
            t = t + '中午好'
        elif time.localtime(time.time()).tm_hour < 17:
            t = t + '下午好'
        elif time.localtime(time.time()).tm_hour < 18:
            t = t + '傍晚好'
        elif time.localtime(time.time()).tm_hour < 21:
            t = t + '晚上好'
        elif time.localtime(time.time()).tm_hour < 23:
            t = t + '夜晚好'
        else:
            t = t + '夜深了'
        t = t + '，当前时间 ' + str(time.localtime(time.time()).tm_hour) + '点' + str(time.localtime(time.time()).tm_min)\
                + '分'
        msg.append(t)
        w = pyweathercn.Weather('哈尔滨')
        msg.append('今天天气 ' + w.today() + ' ' + w.tomorrow())
        msg.append(w.tip())

    if img:
        img_list = get_all_img_name('img/')
        imsg.append(random.choice(img_list))

    Broadcast(msg, imsg).send_broadcast()
    threading.Timer(second + minute * 60 + hour * 3600 + day * 86400, module_repeat,
                    [text, img, second, minute, hour, day]).start()


def broadcast_minus():
    constant.bot.file_helper.send('Time ' + time.asctime(time.localtime(time.time())))
    threading.Timer(30, broadcast_minus).start()


def get_all_img_name(dirpath):
    postfix = ['png', 'jpg']  # 设置要保存的文件格式
    img_list = []
    for maindir, subdir, file_name_list in os.walk(dirpath):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)
            #if True:  # 保存全部文件名。若要保留指定文件格式的文件名则注释该句
            if apath.split('.')[-1] in postfix:   # 匹配后缀，只保存所选的文件格式。若要保存全部文件，则注释该句
                try:
                    img_list.append(apath)
                except:
                    pass  # 所以异常全部忽略即可
    return img_list
