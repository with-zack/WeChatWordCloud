# Usage:
# 将subject改为需要保存聊天记录的人的昵称，注意是昵称而不是你自己设置的备注
# 运行该脚本，会弹出一个二维码图片，扫码登录微信即可
# ta发给你的信息将保存到FROM.txt这个文件里，你发给ta的信息将保存到TO.txt这个文件里
# 该程序的本质是从网页版微信中拉取数据，所以不会有隐私泄露的风险
# 由于微信加密了数据库，我们是无法直接读取以往的聊天记录的
# 只能用这种方式将聊天记录保存到文件中
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
