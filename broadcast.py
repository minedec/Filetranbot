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
from datetime import datetime
from datetime import timedelta


global isRepeat
isRepeat = constant.isRepeat


class Broadcast:
    """
    广播类，包含待发送消息和图片地址列表
    """
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

            # 如果图片体积太大，可能会发送失败
            # 所以这里缺少减小图片体积处理
            # TODO 减小图片体积
            for img_path in self.__img:
                try:
                    value.send_image('%s' % img_path)
                except Exception:
                    continue


def start_repeat(broadcast=None, second=0, minute=0, hour=0, day=0):
    """
    向广播列表中间隔发送广播，广播内容相同
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
    """
    停止广播
    :return:
    """
    global isRepeat
    isRepeat = False


global start_time
start_time = None


def module_set_timer(year=0, month=0, day=0, hour=0, minute=0, second=0):
    from datetime import datetime
    global start_time
    try:
        start_time = datetime(year, month, day, hour, minute, second)
    except Exception:
        constant.bot.file_helper.send('广播启动时间格式错误')
        return
    constant.bot.file_helper.send('启动时间：' + str(start_time))


def module_broadcast(text=False, img=False, second=0, minute=0, hour=0, day=0):
    """
    发送广播，包含天气、时间信息
    :param text: 广播消息是否包含文字
    :param img: 是否包含图片
    :param second: 间隔秒
    :param minute: 间隔分
    :param hour: 间隔时
    :param day: 间隔天
    :return:
    """
    try:
        from datetime import datetime
        global start_time
        if start_time is None:
            constant.bot.file_helper.send('请设置启动时间')
            return
        if (start_time + timedelta(hours=-8)).__le__(convert_to_utc(datetime.now())):
            constant.bot.file_helper.send('启动时间不应早于当前时间')
            return
        threading.Thread(
            target=module_wait,
            args=[text, img, second, minute, hour, day]
        ).start()
    except Exception:
        constant.bot.file_helper.send('启动失败')


def module_wait(text=False, img=False, second=0, minute=0, hour=0, day=0):
    global start_time
    threading.Timer(
        ((start_time + timedelta(hours=-8)) - convert_to_utc(datetime.now())).seconds, module_repeat,
        [text, img, second, minute, hour, day]
    ).start()


def module_repeat(text=False, img=False, second=0, minute=0, hour=0, day=0):
    msg = []
    imsg = []
    if text:
        t = ''
        c_hour = (datetime.utcfromtimestamp(time.time()) + timedelta(hours=8)).hour
        if c_hour < 6:
            t = t + '凌晨好'
        elif c_hour < 8:
            t = t + '早上好'
        elif c_hour < 12:
            t = t + '上午好'
        elif c_hour < 13:
            t = t + '中午好'
        elif c_hour < 17:
            t = t + '下午好'
        elif c_hour < 18:
            t = t + '傍晚好'
        elif c_hour < 21:
            t = t + '晚上好'
        elif c_hour < 23:
            t = t + '夜晚好'
        else:
            t = t + '夜深了'
        t = t + '，当前时间 ' + (
                datetime.utcfromtimestamp(time.time())
                + timedelta(hours=8)
        ).strftime("%Y-%m-%d %H:%M:%S")
        msg.append(t)
        w = pyweathercn.Weather('哈尔滨')
        msg.append('今天天气 ' + w.today() + ' ' + w.tomorrow())
        msg.append(w.tip())

    if img:
        # 检测文件夹是否存在
        if not os.path.exists('img'):
            os.makedirs('img')
        img_list = get_all_img_name('img/')
        imsg.append(random.choice(img_list))

    Broadcast(msg, imsg).send_broadcast()
    if isRepeat:
        threading.Timer(
            second + minute * 60 + hour * 3600 + day * 86400, module_repeat,
            [text, img, second, minute, hour, day]
        ).start()


def broadcast_minus():
    constant.bot.file_helper.send('Time ' + time.asctime(time.localtime(time.time())))
    threading.Timer(30, broadcast_minus).start()


def get_all_img_name(dirpath):
    """
    获得指定目录下所有png，jpg格式文件路径
    :param dirpath: 指定搜索目录
    :return:
    """
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


def get_current_china_time():
    """
    获取当前时刻的中国时区时间
    :return: 中国时区的datetime
    """
    from datetime import datetime, timedelta, timezone
    utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    cn_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
    return cn_dt


def convert_to_utc(local_st):
    """
    本地时间转UTC时间（-8: 00）
    """
    time_struct = time.mktime(local_st.timetuple())
    utc_st = datetime.utcfromtimestamp(time_struct)
    return utc_st
