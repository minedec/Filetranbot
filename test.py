import itchat
import wrshell


@itchat.msg_register(itchat.content.TEXT, isFriendChat=True)
def filehelper_shell(msg):
    if msg['ToUserName'] != 'filehelper':
        return
    print(msg['Text'])
    print(msg['FromUserName'])
    wrshell.inner_func(msg['Text'])


@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def g_r(msg):
    print(msg['Text'])
    print(msg['FromUserName'])


itchat.auto_login(hotReload=True)
friend = itchat.get_friends()
for f in friend:
    print(f)
itchat.run()