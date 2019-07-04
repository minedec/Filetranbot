"""
自动回复模块
"""
import wxpy


def auto_reply(msg):
    #msg.sender.send('开发中....')
    reply = msg.text
    reply = reply.replace('?', '!')
    reply = reply.replace('吗', '')
    if '我' in msg.text:
        reply = reply.replace('我', '你')
    elif '你' in msg.text:
        reply = reply.replace('你', '我')
    return '开发中....\n' + reply
