import urllib.request as ur
import ssl
import json
import time
import re
import smtplib
from email.mime.text import MIMEText
def sendmail(title,neirong):
    username_send = '3118184937@qq.com'  # 邮箱用户名
    password = 'jmajdehdtznjdhca'  # pop3/smtp授权码
    username_recv = '3118184937@qq.com'  # 收件人，多个收件人用逗号隔开
    mail = MIMEText(neirong)
    mail['Subject'] = title
    mail['From'] = username_send  # 发件人
    mail['To'] = username_recv  # 收件人
    #163邮箱服务器smtp.163.com,post=25
    smtp=smtplib.SMTP_SSL('smtp.qq.com',port=465) #QQ邮箱的服务器和端口号
    smtp.login(username_send, password)  # 登录邮箱
    smtp.sendmail(username_send, username_recv, mail.as_string())  # 参数分别是发送者，接收者，第三个是把上面的发送邮件的内容变成字符串
    smtp.quit()  # 发送完毕后退出smtp
def signIn(token,data_dict):
    url = 'https://api.moguding.net:9000/attendence/clock/v1/save'  #签到提交信息链接
    #提交头信息
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json; charset=UTF-8',
        'roleKey': 'student'
    }   
    data=json.dumps(data_dict)#将数据转换为str格式
    requests=ur.Request(url=url,data=data.encode("utf-8"),headers=headers)  #数据提交
    try:
        if json.loads(ur.urlopen(requests,context=context).read().decode())['code']==200:  #判断是否提交成功
            pass
        else:
            sendmail('蘑菇丁','签到失败账号：')
    except Exception as e: #抛出异常
        sendmail('蘑菇丁','签到失败账号：')
        pass
def login(login_data,data_dict):
    request_login = ur.Request(
        url = 'https://api.moguding.net:9000/session/user/v1/login', #登录蘑菇丁
        data =json.dumps(login_data).encode(),#编码字符串
        #登录蘑菇丁头信息
        headers = {
            'Content-Type':'application/json; charset=UTF-8'
        }
    )
    try:
        token = json.loads(ur.urlopen(request_login,context=context).read().decode())['data']['token'] #进行登录
        if token:
            signIn(token,data_dict)
    except Exception as e:   #异常处理
        datad = '<urlopen error Remote end closed connection without response>'
        if datad==str(e):
            print('网络连接超时')
        else:
            sendmail('蘑菇丁','账号密码错误：')
        pass
def  readjson():
    rjson=open('mg.json',encoding='utf-8')
    res=rjson.read()
    datum=json.loads(res) #将str转化成dict格式。
    a=1
    while a<=2:  #循环读取json文件数据 几个账号填写账号的2倍
        data_dict=datum[str(a)]['data_dict']
        login_data=datum[str(a)]['login_data']
        login(login_data,data_dict)
        a+=1
        time.sleep(16) #休眠
        
if __name__ == '__main__':
    context = ssl._create_unverified_context()
    readjson()
    sendmail('蘑菇丁','签到成功：')