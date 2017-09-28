#!/usr/bin/env python3
# LHQ 2017-05-28
# mock httpserver
# 假的 http服务器，任何URL都返回成功

import os
import time
import sys
import json
import argparse

import bottle
from bottle import route, run, template, get, post, static_file, default_app, view,request,redirect,install,response
from bottle import request, install, TEMPLATE_PATH, TEMPLATES, get, redirect
from beaker.middleware import SessionMiddleware

root_dir = os.getcwd()
assets_dir = os.path.join(root_dir, "static")


@get('/static/<filepath:path>')
def sys_static(filepath):
    return static_file(filepath, root=assets_dir)


@route('/<url:path>',method=['GET','POST','PUT','DELETE'])
def callback(url):
    time.sleep(int(args.sleep))
    url = url.replace('/','_')
    _method = request.method.lower()
    _file = f'{url}_{_method}.txt'
    if args.verbose:
        print(f'Read file:{_file}')
    if os.path.isfile(_file):
        with open(_file) as f:
            return json.loads(f.read())
    return {"resid":0,"resmsg":""}

def reqrspwatch(callback):
    def wrapper(*args, **kwargs):
        print('----Request Header---- %s' % request.path)
        for x, y in request.headers.items():
            print('%s=%s' % (x, y))
        if request.headers.get('content-type') == 'application/json':
            print('----Request Body---- %s' % request.path)
            print(json.dumps(request.json, ensure_ascii=False, indent=4))
        x =request._get_body_string().decode()
        print('------原始post内容------')
        print(x)
        body = callback(*args, **kwargs)
        print('----Response Header----')
        for x, y in response.headers.items():
            print('%s=%s' % (x, y))
        print('----Response Body----')
        try:
            print(json.dumps(body, ensure_ascii=False, indent=4))
        except:
            pass
        return body
    return wrapper

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-V','--verbose',nargs='?',help='显示详细请求响应内容',default=False,required=False,type=bool)
    parser.add_argument('-p','--port',nargs='?',help='监听的端口',default='8000',required=False)
    parser.add_argument('-s','--sleep',nargs='?',help='请求的延迟响应秒数',default=0,required=False)
    args = parser.parse_args()
    if args.verbose:
        print('详细模式')
        install(reqrspwatch)
    app = default_app()
    run(app=app,host='0.0.0.0', port=int(args.port), debug=True, reloader=True)
