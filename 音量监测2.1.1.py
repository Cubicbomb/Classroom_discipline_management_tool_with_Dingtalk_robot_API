import tkinter as tk
import json
import hashlib
import base64
import hmac
import os
import time
import requests
from urllib.parse import quote_plus
import pyaudio
import numpy as np

win=tk.Tk()
win.geometry("600x300")#大小
win.title("Cb音量检测系统")#标题

#th阈值，nt信息，tes测试
jiwei=tk.StringVar()

#本段代码（从此处起到第42行）修改自Python实用宝典：https://pythondict.com
#原文链接：https://blog.csdn.net/u010751000/article/details/121313045
class Messenger:
    def __init__(self, token=os.getenv("DD_ACCESS_TOKEN"), secret=os.getenv("DD_SECRET")):
        self.timestamp = str(round(time.time() * 1000))
        self.URL = "https://oapi.dingtalk.com/robot/send"
        self.headers = {'Content-Type': 'application/json'}
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(self.timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        self.sign = quote_plus(base64.b64encode(hmac_code))
        self.params = {'access_token': token, "sign": self.sign}
        
    def send_markdown(self, title, text):
        data = {"msgtype": "markdown", "markdown": {"title":title,"text":text}}
        self.params["timestamp"] = self.timestamp
        return requests.post(
            url=self.URL,
            data=json.dumps(data),
            params=self.params,
            headers=self.headers
        )


def audioCheck(): # 麦克风检测
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK)#打开声卡，设置 采样深度、通道数、采样率、输入和采样点缓存数量
    data = stream.read(CHUNK)#以CHUNK读取音频数据
    audio_data = np.frombuffer(data,dtype=np.short)#音频处理，比如【123456】变成【【12】【34】【56】】
    max_dB = np.max(audio_data)#取每组最大值
    return max_dB

def renew():
    global m,tke,scr
    tke=str(tok.get('1.0','end'))
    tke=tke.rstrip("\n")
    scr=str(sec.get('1.0','end'))
    scr=scr.rstrip("\n")
    if tke=="" and scr=="":#没有主动填写
        with open(r'data.txt','a+',encoding='UTF-8',errors='ignore') as data:
            data.seek(0,0)
            tns=data.read()
        if tns != '':#data有过记录
            tns=tns.split('\n')
            tke=str(tns[0])
            scr=str(tns[1])
            tok.insert('1.0',tke)
            sec.insert('1.0',scr)
        else:#data没有记录
            nt.insert(tk.CURRENT,"请填写token与密钥")
    elif tke != "" and scr == "":
        nt.insert(tk.CURRENT,"请填写密钥")
    elif tke == "" and scr != "":
        nt.insert(tk.CURRENT,"请填写token")
    else:#主动填写
        with open(r'data.txt','a+',encoding='UTF-8',errors='ignore') as data:
            data.seek(0,0)
            data.truncate(0)
            data.write(tke+'\n')
            data.write(scr+'\n')
    m = Messenger(token=str(tke),secret=str(scr))
#加入所需


def test():
    nt.insert(tk.CURRENT,"当前音量为："+str(audioCheck()))
def forest():
    global doid
    def tototo():
        global doid
        gth=th.get('1.0','end')#th得到
        mx_set=int(float(gth))
        audio=audioCheck()
        print("on",audio)
        jiwei.set(audio)
        if gth=="":
            nt.insert(tk.CURRENT,"阈值不能为空")
        elif audio>=mx_set:
            m.send_markdown(
                title="音量监测报警信息:",
                text="### 音量监测报警信息： \n\n"
                    "#### 当前音量达到阈值 \n\n"
                    "> 阈值："+str(mx_set)+" \n\n"
                    "> 当前音量："+str(audio)+"\n\n"
            )
            nt.insert(tk.CURRENT,"警告已发出")
        doid=win.after(1000,tototo)
    tototo()
def end():
    win.after_cancel(doid)
    nt.delete('1.0','end')#nt清空
    jiwei.set("停止")



th=tk.Text(win)
nt=tk.Text(win)
tok=tk.Text(win)
sec=tk.Text(win)
tok_Label=tk.Label(win,text="token：")
sec_Label=tk.Label(win,text="密钥：")
renew_Button=tk.Button(win,text="获取/刷新",command=renew)
f=tk.Label(win,text="信息：")
tes=tk.Button(win,text="监测",command=test)
bgn=tk.Button(win,text="开始",command=forest)
ed=tk.Button(win,text="结束",command=end)
c=tk.Label(win,text="阈值：")
f=tk.Label(win,text="信息：")
wyx= tk.Label(win,textvariable=jiwei,fg='blue',font=("黑体",100))

    



th.place(x=100,y=10,width=150,height=20)#x，y是左上点坐标，w，h是宽度
nt.place(x=100,y=50,width=150,height=80)

tok.place(x=75,y=300,width=480,height=20)
sec.place(x=75,y=340,width=480,height=20)
tok_Label.place(x=20,y=300,width=50,height=20)
sec_Label.place(x=20,y=340,width=50,height=20)
renew_Button.place(x=50,y=380,width=70,height=30)

tes.place(x=50,y=140,width=150,height=20)
bgn.place(x=50,y=170,width=150,height=20)
ed.place(x=50,y=200,width=150,height=20)
c.place(x=50,y=10,width=50,height=20)
f.place(x=50,y=50,width=50,height=20)
wyx.place(x=300,y=20)

win.mainloop()

#Copyright (c) 2024 Cubicbomb