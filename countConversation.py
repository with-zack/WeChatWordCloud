import itchat
subject = '没有人问过莱卡' #需要记录的对象的昵称
@itchat.msg_register(itchat.content.TEXT)
def print_content(msg):
    user = msg['User']
    if(user['NickName']==subject):
        # 如果是该对象发来的消息或者发往该对象的消息
        if(user['UserName']==msg['FromUserName']):
            # 该对象发来的消息
            with open("FROM.txt", "a", encoding="utf-8") as text_file:
                print("{}".format(msg['Text']), file=text_file)
        else:
            # 发往该对象的消息
            with open("TO.txt", "a", encoding="utf-8") as text_file:
                print("{}".format(msg['Text']), file=text_file)
itchat.auto_login(hotReload=True)
itchat.run()
