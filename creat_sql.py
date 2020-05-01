#!/usr/bin/env python
# _*_coding:utf-8 _*_
#@Time    :   13:03
#@Auther  :Jarrett
#@FileName: creat_sql.py
#@Software: PyCharm

import sqlite3

conn = sqlite3.connect('database.db')
print("Opened database successfully")

conn.execute('CREATE TABLE students (name TEXT, addr TEXT, city TEXT, pin TEXT)')
print('Table created successfully')
conn.close()