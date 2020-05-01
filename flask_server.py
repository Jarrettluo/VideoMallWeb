#!/usr/bin/env python
# _*_coding:utf-8 _*_
# @Time    :   9:03
# @Auther  :Jarrett
# @FileName: flask_server.py
# @Software: PyCharm
from re import escape

from flask import Flask, url_for, request, render_template, session, flash
from werkzeug.utils import redirect

import sqlite3 as sql
from forms import ContactForm

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
# MySQL的默认端口是3306，天上之前创建的数据库名
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'

DIALCT = "mysql"
DRIVER = "pymysql"
USERNAME = "root"
PASSWORD = "admin"
HOST = "127.0.0.1"
PORT = "3306"
DATABASE = "flask_sqlalchmy_demo"
DB_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALCT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)
#app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI


#设置这一项是每次请求结束后都会自动提交数据库中的变动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
# 一次更新多个配置值可以使用dict.update()方法
app.config.update(
    TESTING=True,
    SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/'   # 这里登录的是root用户，要填上自己的密码
)

db = SQLAlchemy(app)   # 实例化

class students(db.Model):
    id = db.Column('student_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    addr = db.Column(db.String(200))
    pin = db.Column(db.String(10))

    def __init__(self, name, city, addr, pin):
        self.name = name
        self.city = city
        self.addr = addr
        self.pin = pin
        db.create_all()  #要创建/使用URI中提及的数据库，请运行create_all()方法。


@app.route('/')
@app.route('/index')
def hello_world():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])  # escape 是用来转义的。
    return 'Hello, World! You are not logged in!'


@app.route('/hello')
def hello():
    return render_template('hello.html', name=name)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
        pass
        # return do_the_login()
    else:
        pass
        # return show_the_login_form()


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/projects/')
def projects():
    return 'The project page'


@app.route('/about')
def about():
    return 'The about page'


@app.route('/user/<username>')
def profile(username):
    return '{}\'s profile'.format(escape(username))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@app.route("/me")
def me_api():
    user = get_current_user()
    return {
        "username": user.username,
        "theme": user.theme,
        "image": url_for("user_image", filename=user.image),
    }


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('contact.html', form=form)
        else:
            return render_template('success.html')
    elif request.method == 'GET':
        return render_template('contact.html', form=form)


@app.route('/enternew')
def new_student():
    return render_template('student.html')


@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            nm = request.form['nm']
            addr = request.form['add']
            city = request.form['city']
            pin = request.form['pin']

            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO students (name, addr, city, pin) VALUES(?, ?, ?, ?)", (nm, addr, city, pin))
                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("result.html", msg=msg)
            con.close()
    else:
        return render_template('student.html')


@app.route('/list')
def list():
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from students")

    rows = cur.fetchall();
    return render_template("list.html", rows=rows)


@app.route('/show_all')
def show_all():
    return render_template('show_all.html', students=students.query.all())


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        print("heeee")
        if not request.form['name'] or not request.form['city'] or not request.form['addr']:
            flash('Please enter all the fields', 'error')
        else:
            student = students(request.form['name'], request.form['city'],
                               request.form['addr'], request.form['pin'])

            db.session.add(student)   # (模型对象) - 将记录插入到映射表中
            db.session.commit()

            flash('Record was successfully added')
            return redirect(url_for('show_all'))
    return render_template('new.html')


"""
with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))
"""
if __name__ == '__main__':
    app.run()
