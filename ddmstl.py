#创建机器人时选加签
import json
import hashlib
import base64
import hmac
import os
import time
import requests
from urllib.parse import quote_plus
 
 
class Messenger:
    def __init__(self, token=os.getenv("DD_ACCESS_TOKEN"), secret=os.getenv("DD_SECRET")):
        self.timestamp = str(round(time.time() * 1000))
        self.URL = "https://oapi.dingtalk.com/robot/send"
        self.headers = {'Content-Type': 'application/json'}
        secret = secret
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(self.timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        self.sign = quote_plus(base64.b64encode(hmac_code))
        self.params = {'access_token': token, "sign": self.sign}
     
    def send_data(self, data):#套格式
        self.params["timestamp"] = self.timestamp
        return requests.post(#标准的套格式东东
            url=self.URL,
            data=json.dumps(data),
            params=self.params,
            headers=self.headers
        )
    
    def send_text(self, content):
        data = {"msgtype": "text", "text": {"content": content}}#真正有用的玩意
        self.send_data(data)
    def send_markdown(self, title, text):
        data = {"msgtype": "markdown","markdown":{"title":title,"text":text}}#真正有用的玩意
        self.send_data(data)
    
#https://open.dingtalk.com/document/orgapp/custom-bot-send-message-type
if __name__ == "__main__":
    m = Messenger(
        token="your_token",#这里填网址后面那一串
        secret="your_SEC"#这里填创建机器人时的密钥
    )
    #m.send_text("aa")
    m.send_markdown(
        title="实践时间已确定，尽快查看",
        text="# 当前进度同步 \n\n"
        "### 实践地点确定为： \n\n"
        "> 海宁市第三人民医院 \n\n"
        "### 实践方式拟确定为： \n\n"
        "> 全员线下 \n\n"
        "### 实践时间已确定为： \n\n"
        "> 7月11日下午 \n\n"
        "### 下一步待定： \n\n"
        "- 制定拍摄任务与分工 \n\n"
        "#### 请尽快查看消息并回复“线下”确认线下参与，如果"
        "**无法线下参与**"
        "请及时告知 \n\n"
        "##### 7月10日12点后没有回复的，默认线上参与 \n\n"
        "### 后续还需要： \n\n"
        "- 制定拍摄任务与分工 \n\n"
        "- 线下组时空细节确定 \n\n"
        "###### 请务必及时关注本群消息"
    )
    

#markdown语法等参见钉钉机器人官方文档，部分代码修改自https://github.com/Ckend/dd_notice
#Copyright (c) 2024 Cubicbomb