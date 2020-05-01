#!/usr/bin/env python
# _*_coding:utf-8 _*_
#@Time    :   9:03
#@Auther  :Jarrett
#@FileName: flask_server.py
#@Software: PyCharm

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'