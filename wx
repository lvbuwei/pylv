# coding:utf-8
# 发送消息到微信小助手

import json

from bottle import get, request
import requests

# 微信小程序登录参数
#WXKEY = 'XXXXXXX' # 18位的key
#WXSECRET = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' # 64位字符长度的的Secret

def get_token():
    url='https://qyapi.weixin.qq.com/cgi-bin/gettoken'
    values = {'corpid' : WXKEY ,
            'corpsecret': WXSECRET,
            }
    req = requests.post(url, params=values)
    data = json.loads(req.text)
    return data["access_token"]

@get('/api/wx/sendmsg/')
def send_wxmsg():
    _user = (request.query.user or '').strip()
    _part = (request.query.part or '').strip()
    _encrypt = (request.query.encrypt or '').strip()
    if _encrypt not in ['1','0']:
        _encrypt = '0'
    _content = (request.query.content or '').strip()
    if _user == '' and _part == '':
        return {"resid":-1,"resmsg":"用户或组不能都为空"}
    if _content == '':
        return {"resid":-2,"resmsg":"内容为空"}
    url="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="+get_token()
    values = """{"touser" : "%s" ,
            "toparty":"%s",
            "msgtype":"text",
            "agentid":"1000005",
            "text":{
                "content": "%s"
            },
            "safe":"%s"
            }""" % (_user,_part,_content,_encrypt)
  
    headers = {"Content-Type":"application/json; charset=UTF-8"}
    req = requests.post(url, values.encode())
    _json = json.loads(req.text)
    _json['resmsg']=0
    _json['resmsg']='发送完成'
    return _json

if __name__ == '__main__':
    from bottle import default_app,run
    app = default_app()
    run(app, host='0.0.0.0', port=7080, debug=True, reloader=True)
