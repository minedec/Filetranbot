"""
初始化聊天机器人模块
"""
from wxpy import *
import wrshell
import broadcast
import constant
import time
import os

bot = Bot(cache_path=True)
bot.enable_puid()
constant.bot = bot


@bot.register(None, TEXT, except_self=False)
def file_helper_shell(msg):
    print(msg)
    if msg.receiver != bot.file_helper:
        return
    wrshell.inner_func(msg.text)


@bot.register(Friend, TEXT)
def friend_reply(msg):
    if msg.receiver.puid not in constant.contact_friend_list.keys():
        return
    return


@bot.register(Group, TEXT)
def group_reply(msg):
    if msg.receiver.puid not in constant.contact_group_list.keys():
        return
    return


#constant.deliver_list.update({bot.file_helper.puid: bot.file_helper})
#broadcast.module_repeat(True, True, 10)

constant.deliver_list.update({bot.file_helper.puid: bot.file_helper})
broadcast.module_broadcast(True, True, 20)

embed()
#bot.join()

