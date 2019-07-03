"""
初始化聊天机器人模块
"""
from wxpy import *
import wrshell
import broadcast

global bot
bot = Bot(cache_path=True)
bot.enable_puid()
wrshell.set_bot(bot)


@bot.register(None, TEXT, except_self=False)
def file_helper_shell(msg):
    print(msg)
    if msg.receiver != bot.file_helper:
        return
    wrshell.inner_func(msg.text)


@bot.register(Friend, TEXT)
def friend_reply(msg):
    if msg.receiver.puid not in wrshell.contact_friend_list.keys():
        return
    return


@bot.register(Group, TEXT)
def group_reply(msg):
    if msg.receiver.puid not in wrshell.contact_group_list.keys():
        return
    return


broadcast.set_bot(bot)
broadcast.broadcast_minus()
embed()
#bot.join()

