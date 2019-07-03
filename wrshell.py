"""
小型shell模块，使用文件传输助手作为shell
解析输入命令行，提供函数供调用
命令行包含
添加好友到活动列表中
    wr -addf <friend_name>
    -添加好友到活动列表中，添加到活动列表中的好友提供图片查询和其他功能
    -非活动列表中的好友不提供任何功能

删除活动列表中好友
    wr -rmf <friend_name>
    -从活动列表中删除好友，不再提供相关功能

显示活动列表中好友
    wr -lf
    - 显示活动列表中好友

添加群组到活动列表中
    wr -addg <group_name>
    -添加群组到活动列表中，群组中的所有人可以使用账号的图片查询和其他功能

删除活动列表中的群组
    wr -rmg <group_name>
    -删除群组，不再提供相关功能

显示活动列表中的群组
    wr -lg
    - 显示活动列表中群组

添加图片到图片缓存中
    wr -addimg
    -添加图片到图片缓存中，使用者可以发出相关指令查询图片缓存中的图片
    -输入添加图片命令后，5分钟内发往文件助手的图片都存入图片缓存中

显示帮助
    wr -h
"""
from wxpy import *
from threading import Thread
import time

# 好友活动列表
global contact_friend_list
contact_friend_list = {}

# 群组活动列表
global contact_group_list
contact_group_list = {}

# 图片缓存文件夹
global img_path
img_path = 'img/'

global isReceive
isReceive = False

global bot    # self bot


def set_bot(new_bot):
    global bot
    bot = new_bot


def get_contact_friend():
    global contact_friend_list
    return contact_friend_list


def get_contact_group():
    global contact_group_list
    return contact_group_list


def inner_func(command):
    """
    判断是否是内置命令，内置命令以wr开头
    :param command: 命令行
    :return: 无
    """
    args = command.strip().split(' ')
    if args[0] == 'wr':
        execute_func(args)


def add_img(args=None):
    """
    添加图片缓存
    :return:
    """
    print('Start receving...')
    bot.file_helper.send('开始接收图片，5分钟内有效')
    thread = Thread(target=receive_cache)
    thread.start()


# set timer in 5 min
def stop_cache():
    """
    停止图片缓存
    :return:
    """
    print('Start timer...')
    time.sleep(300)
    global isReceive
    isReceive = False
    bot.file_helper.send('5分钟已到，停止接收图片')
    print('Stop timer...')


def receive_cache():
    """
    添加图片到图片缓存文件夹中，5分钟内有效
    :return: 无
    """
    global isReceive
    isReceive = True
    print('Start caching...')

    @bot.register(None, PICTURE, except_self=False)
    def filehelper_img_cache(msg):
        if not isReceive:
            return
        if msg.receiver != bot.file_helper:
            return
        msg.get_file(img_path + msg.file_name)
        bot.file_helper.send('收到图片：' + msg.file_name)

    thread_02 = Thread(target=stop_cache)    # start timer
    thread_02.start()


def add_friend(args=None):
    """
    向活动列表中添加好友，仅向处于活动列表中的好友提供自动回复
    :param args: 命令行参数
    :return: 无
    """
    friend_name = args[2]
    friend = bot.friends().search(friend_name)[0]
    if friend is None:
        bot.file_helper.send('未找到 ' + friend_name)
    global contact_friend_list
    contact_friend_list.update({friend.puid: friend})
    bot.file_helper.send('添加 ' + friend.name)


def remove_friend(args=None):
    """
    移除活动列表中的好友
    :param args: 命令行参数，包含移除好友名称
    :return: 无
    """
    friend_name = args[2]
    friend = bot.friends().search(friend_name)[0]
    if friend is None:
        bot.file_helper.send('未找到 ' + friend_name)
    if friend.puid in contact_friend_list.keys():
        contact_friend_list.pop(friend.puid)
        bot.file_helper.send('已删除 ' + friend.name)


def show_friends(args=None):
    """
    展示活动列表中好友
    :param args: 命令行参数
    :return: 无
    """
    name_list = []
    for i in contact_friend_list.keys():
        name_list.append(contact_friend_list.get(i).name)
    if name_list:
        bot.file_helper.send('\n'.join(name_list))
    else:
        bot.file_helper.send('列表为空')


def add_group(args=None):
    """
    向活动列表中添加群组，仅向处于活动列表中的群组提供自动回复
    :param args: 命令行参数，包含群组名称
    :return: 无
    """
    group_name = args[2]
    if not bot.groups().search(group_name):
        bot.file_helper.send('未找到 ' + group_name)
    group = bot.groups().search(group_name)[0]
    if group is None:
        bot.file_helper.send('未找到 ' + group_name)
    global contact_group_list
    contact_group_list.update({group.puid: group})
    bot.file_helper.send('添加 ' + group.name)


def remove_group(args=None):
    """
    移除活动列表中的群组
    :param args: 命令行参数，包含群组名称
    :return: 无
    """
    group_name = args[2]
    group = bot.friends().search(group_name)[0]
    if group is None:
        bot.file_helper.send('未找到 ' + group_name)
    if group.puid in contact_group_list.keys():
        contact_group_list.pop(group.puid)
        bot.file_helper.send('已删除 ' + group.name)


def show_groups(args=None):
    """
    展示活动列表中的群组
    :param args: 命令行参数
    :return: 无
    """
    name_list = []
    for i in contact_group_list.keys():
        name_list.append(contact_group_list.get(i).name)
    if name_list:
        bot.file_helper.send('\n'.join(name_list))
    else:
        bot.file_helper.send('列表为空')


def show_help(args=None):
    """
    显示帮助
    :param args: 命令行参数
    :return:
    """
    help_info = 'wr <option> <**args> \n   -addf <friend_name> 添加好友 \n'\
                '   -rmf <friend_name> 删除好友 \n   -lf 显示名单好友 \n'\
                '   -addg <group_name> 添加群组 \n   -rmg 删除群组\n'\
                '   -lg 显示名单群组\n   -addimg 添加图片缓存\n   -h 显示帮助'
    bot.file_helper.send(help_info)


func_dict = {
    '-h': show_help,
    '-addimg': add_img,
    '-addf': add_friend,
    '-rmf': remove_friend,
    '-lf': show_friends,
    '-addg': add_group,
    '-rmg': remove_group,
    '-lg': show_groups
}


def execute_func(args):
    """
    执行内置命令功能
    :param args: 命令行参数
    :return: 无
    """
    func = func_dict[args[1]]
    if func is None:
        return
    func(args)




