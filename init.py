"""
初始化聊天机器人模块
"""
from wxpy import *
import wrshell
import broadcast
import constant
import auto_reply
import time
import os

bot = Bot(cache_path=True)
bot.enable_puid()
constant.bot = bot


@bot.register(bot.file_helper, TEXT, except_self=False)
def file_helper_shell(msg):
    print(msg)
    if msg.receiver != bot.file_helper:
        return
    wrshell.inner_func(msg.text)


@bot.register(Friend, TEXT)
def friend_reply(msg):
    print(msg)
    if msg.sender.puid not in constant.contact_friend_list.keys():
        return
    return auto_reply.auto_reply(msg)


@bot.register(Group, TEXT)
def group_reply(msg):
    if msg.sender.puid not in constant.contact_group_list.keys():
        return
    if not msg.is_at:
        return
    return auto_reply.auto_reply(msg)


embed()
#bot.join()

