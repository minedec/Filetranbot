import itchat
import wrshell
import os
import time
import pyweathercn

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
def get_all_img_name(dirpath):
    postfix = ['png', 'jpg']  # 设置要保存的文件格式
    img_list = []
    for maindir, subdir, file_name_list in os.walk(dirpath):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)
            #if True:  # 保存全部文件名。若要保留指定文件格式的文件名则注释该句
            if apath.split('.')[-1] in postfix:   # 匹配后缀，只保存所选的文件格式。若要保存全部文件，则注释该句
                try:
                    print(apath)
                except:
                    pass  # 所以异常全部忽略即可

get_all_img_name('img/')
#itchat.run()