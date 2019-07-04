"""
小型shell模块，使用文件传输助手作为shell
解析输入命令行，提供函数供调用
命令行包含
添加好友到活动列表中
    wr addf <friend_name>
    -添加好友到活动列表中，添加到活动列表中的好友提供图片查询和其他功能
    -非活动列表中的好友不提供任何功能

删除活动列表中好友
    wr rmf <friend_name>
    -从活动列表中删除好友，不再提供相关功能

显示活动列表中好友
    wr lf
    - 显示活动列表中好友

添加群组到活动列表中
    wr addg <group_name>
    -添加群组到活动列表中，群组中的所有人可以使用账号的图片查询和其他功能

删除活动列表中的群组
    wr rmg <group_name>
    -删除群组，不再提供相关功能

显示活动列表中的群组
    wr lg
    - 显示活动列表中群组

添加图片到图片缓存中
    wr addimg
    -添加图片到图片缓存中，使用者可以发出相关指令查询图片缓存中的图片
    -输入添加图片命令后，5分钟内发往文件助手的图片都存入图片缓存中

添加好友或群组到广播列表中
    wr addb <friend_name or group_name>
    -添加好友或群组到广播列表中，每天收到广播

删除广播列表中好友或群组
    wr rmb <friend_name or group_name>
    -将好友或群组从广播列表中移除

显示广播列表中的好友或群组
    wr lb
    - 显示活动列表中好友或群组

开始广播，指定间隔秒，分，时，天，空格分开，可以选择填写
    wr onb <second> <minute> <hour> <day>

关闭广播
    wr offb

显示帮助
    wr h
"""
from wxpy import *
from threading import Thread
import time
import constant
import broadcast


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
    constant.bot.file_helper.send('开始接收图片，5分钟内有效')
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
    constant.bot.file_helper.send('5分钟已到，停止接收图片')
    print('Stop timer...')


def receive_cache():
    """
    添加图片到图片缓存文件夹中，5分钟内有效
    :return: 无
    """
    global isReceive
    isReceive = True
    print('Start caching...')

    @constant.bot.register(None, PICTURE, except_self=False)
    def filehelper_img_cache(msg):
        if not isReceive:
            return
        if msg.receiver != constant.bot.file_helper:
            return
        msg.get_file(constant.img_path + msg.file_name)
        constant.bot.file_helper.send('收到图片：' + msg.file_name)

    thread_02 = Thread(target=stop_cache)    # start timer
    thread_02.start()


def add_friend(args=None):
    """
    向活动列表中添加好友，仅向处于活动列表中的好友提供自动回复
    :param args: 命令行参数
    :return: 无
    """
    friend_name = args[2]
    friend = constant.bot.friends().search(friend_name)[0]
    if friend is None:
        constant.bot.file_helper.send('未找到 ' + friend_name)
    constant.contact_friend_list.update({friend.puid: friend})
    constant.bot.file_helper.send('添加 ' + friend.name)


def remove_friend(args=None):
    """
    移除活动列表中的好友
    :param args: 命令行参数，包含移除好友名称
    :return: 无
    """
    friend_name = args[2]
    friend = constant.bot.friends().search(friend_name)[0]
    if friend is None:
        constant.bot.file_helper.send('未找到 ' + friend_name)
    if friend.puid in constant.contact_friend_list.keys():
        constant.contact_friend_list.pop(friend.puid)
        constant.bot.file_helper.send('已删除 ' + friend.name)


def show_friends(args=None):
    """
    展示活动列表中好友
    :param args: 命令行参数
    :return: 无
    """
    name_list = []
    for i in constant.contact_friend_list.keys():
        name_list.append(constant.contact_friend_list.get(i).name)
    if name_list:
        constant.bot.file_helper.send('\n'.join(name_list))
    else:
        constant.bot.file_helper.send('列表为空')


def add_group(args=None):
    """
    向活动列表中添加群组，仅向处于活动列表中的群组提供自动回复
    :param args: 命令行参数，包含群组名称
    :return: 无
    """
    group_name = args[2]
    if not constant.bot.groups().search(group_name):
        constant.bot.file_helper.send('未找到 ' + group_name)
    group = constant.bot.groups().search(group_name)[0]
    if group is None:
        constant.bot.file_helper.send('未找到 ' + group_name)
    constant.contact_group_list.update({group.puid: group})
    constant.bot.file_helper.send('添加 ' + group.name)


def remove_group(args=None):
    """
    移除活动列表中的群组
    :param args: 命令行参数，包含群组名称
    :return: 无
    """
    group_name = args[2]
    group = constant.bot.friends().search(group_name)[0]
    if group is None:
        constant.bot.file_helper.send('未找到 ' + group_name)
    if group.puid in constant.contact_group_list.keys():
        constant.contact_group_list.pop(group.puid)
        constant.bot.file_helper.send('已删除 ' + group.name)


def show_groups(args=None):
    """
    展示活动列表中的群组
    :param args: 命令行参数
    :return: 无
    """
    name_list = []
    for i in constant.contact_group_list.keys():
        name_list.append(constant.contact_group_list.get(i).name)
    if name_list:
        constant.bot.file_helper.send('\n'.join(name_list))
    else:
        constant.bot.file_helper.send('列表为空')


def add_broadcast(args=None):
    """
    向广播列表中添加好友群组，仅向处于广播列表中的群组提供广播
    :param args: 命令行参数，包含名称
    :return: 无
    """
    name = args[2]
    if name == 'file_helper':
        constant.deliver_list.update({constant.bot.file_helper.puid: constant.bot.file_helper})
        constant.bot.file_helper.send('添加 文件传输助手')
        return
    if constant.bot.friends().search(name):
        friend = constant.bot.friends().search(name)[0]
        if friend is not None:
            constant.deliver_list.update({friend.puid: friend})
            constant.bot.file_helper.send('添加 ' + friend.name)
            return
    constant.bot.file_helper.send('未找到好友 ' + name)
    if constant.bot.groups().search(name):
        group = constant.bot.groups().search(name)[0]
        if group is not None:
            constant.deliver_list.update({group.puid: group})
            constant.bot.file_helper.send('添加 ' + group.name)
            return
    constant.bot.file_helper.send('未找到群组 ' + name)


def remove_broadcast(args=None):
    """
    移除广播列表中的好友群组
    :param args: 命令行参数，包含名称
    :return: 无
    """
    friend_name = args[2]
    friend = constant.bot.friends().search(friend_name)[0]
    if friend is None:
        constant.bot.file_helper.send('未找到 ' + friend_name)
    if friend.puid in constant.deliver_list.keys():
        constant.deliver_list.pop(friend.puid)
        constant.bot.file_helper.send('已删除 ' + friend.name)
        return
    group_name = args[2]
    group = constant.bot.friends().search(group_name)[0]
    if group is None:
        constant.bot.file_helper.send('未找到 ' + group_name)
    if group.puid in constant.deliver_list.keys():
        constant.deliver_list.pop(group.puid)
        constant.bot.file_helper.send('已删除 ' + group.name)


def show_broadcast(args=None):
    """
    展示广播列表中的好友群组
    :param args: 命令行参数
    :return: 无
    """
    name_list = []
    for i in constant.deliver_list.keys():
        name_list.append(constant.deliver_list.get(i).name)
    if name_list:
        constant.bot.file_helper.send('\n'.join(name_list))
    else:
        constant.bot.file_helper.send('列表为空')


def turn_on_broadcast(args=None):
    if len(args) == 2:
        constant.bot.file_helper.send('设置失败，间隔不能为空')
        return

    second = 0
    minute = 0
    hour = 0
    day = 0

    if len(args) == 3:
        second = int(args[2])
    elif len(args) == 4:
        second = int(args[2])
        minute = int(args[3])
    elif len(args) <= 5:
        second = int(args[2])
        minute = int(args[3])
        hour = int(args[4])
    elif len(args) <= 6:
        second = int(args[2])
        minute = int(args[3])
        hour = int(args[4])
        day = int(args[5])

    constant.isRepeat = True
    constant.bot.file_helper.send('广播已开启，广播对象为')
    show_broadcast()
    broadcast.module_broadcast(True, True, second, minute, hour, day)


def turn_off_broadcast(args=None):
    constant.bot.file_helper.send('广播已关闭')
    broadcast.stop_repeat()


def show_help(args=None):
    """
    显示帮助
    :param args: 命令行参数
    :return:
    """
    help_info = 'wr <option> <**args> \n   addf <friend_name> 添加好友 \n'\
                '   rmf <friend_name> 删除好友 \n   lf 显示名单好友 \n'\
                '   addg <group_name> 添加群组 \n   rmg 删除群组\n'\
                '   lg 显示名单群组\n   addimg 添加图片缓存\n   h 显示帮助\n'\
                '   addb <friend_name | group_name> 添加广播对象\n   rmb <friend_name | group_name> 移除广播对象\n'\
                '   lb 显示广播列表\n   onb <second> <minute> <hour> <day> 开启广播，设置间隔\n'\
                '   offb 关闭广播\n'
    constant.bot.file_helper.send(help_info)


func_dict = {
    'h': show_help,
    'addimg': add_img,
    'addf': add_friend,
    'rmf': remove_friend,
    'lf': show_friends,
    'addg': add_group,
    'rmg': remove_group,
    'lg': show_groups,
    'addb': add_broadcast,
    'rmb': remove_broadcast,
    'lb': show_broadcast,
    'onb': turn_on_broadcast,
    'offb': turn_off_broadcast
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
    print(args)
    func(args)




