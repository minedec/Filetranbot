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
    msg = ''
    imsg = []
    if text:
        if time.localtime(time.time()).tm_hour < 6:
            msg = msg + '凌晨好'
        elif time.localtime(time.time()).tm_hour < 8:
            msg = msg + '早上好'
        elif time.localtime(time.time()).tm_hour < 12:
            msg = msg + '上午好'
        elif time.localtime(time.time()).tm_hour < 13:
            msg = msg + '中午好'
        elif time.localtime(time.time()).tm_hour < 17:
            msg = msg + '下午好'
        elif time.localtime(time.time()).tm_hour < 18:
            msg = msg + '傍晚好'
        elif time.localtime(time.time()).tm_hour < 21:
            msg = msg + '晚上好'
        elif time.localtime(time.time()).tm_hour < 23:
            msg = msg + '夜晚好'
        else:
            msg = msg + '夜深了'

        w = pyweathercn.Weather('哈尔滨')
        msg = msg + ', 今天天气 ' + w.today() + ' ' + w.tomorrow() + '\n' + w.tip()
        msg = [msg]

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
