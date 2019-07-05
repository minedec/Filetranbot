"""
自动回复模块
"""
import wxpy

global isMenu
isMenu = False


def auto_reply(msg):
    #msg.sender.send('开发中....')
    if msg.text == '功能':

        return menu_reply(msg)
    # 如果是功能就调用功能菜单
    # 否则就当复读机
    reply = msg.text
    reply = reply.replace('?', '!')
    reply = reply.replace('吗', '')
    if '我' in msg.text:
        reply = reply.replace('我', '你')
    elif '你' in msg.text:
        reply = reply.replace('你', '我')
    return '开发中....\n' + reply


def menu_reply(msg):
    # TODO 实现不同用户调用菜单区分回复，就是调出菜单用户用菜单模块回复，其余自动回复
    return '功能菜单未完成🙃'
