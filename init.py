"""
初始化聊天机器人模块
"""
from wxpy import *
import wrshell

global bot
bot = Bot(cache_path=True)
bot.enable_puid()
wrshell.set_bot(bot)


@bot.register(None, TEXT, except_self=False)
def filehelper_shell(msg):
    print(msg)
    if msg.receiver != bot.file_helper:
        return
    wrshell.inner_func(msg.text)


@bot.register(Friend, TEXT)
def friend_reply(msg):
    if msg.receiver.puid not in wrshell.contact_friend_list.keys():
        return
    return

embed()
#bot.join()

