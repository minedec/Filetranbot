"""
广播模块
每天复读机
"""
from wxpy import *
import threading
import time

global bot
bot = None


def set_bot(newbot):
    global bot
    bot = newbot


def broadcast_minus():
    bot.file_helper.send('Time ' + time.asctime(time.localtime(time.time())))
    threading.Timer(30, broadcast_minus).start()
