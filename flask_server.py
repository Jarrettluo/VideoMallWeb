#!/usr/bin/env python
# _*_coding:utf-8 _*_
# @Time    :   9:03
# @Auther  :Jarrett
# @FileName: flask_server.py
# @Software: PyCharm
from re import escape

from flask import Flask, url_for, request, render_template, session
from werkzeug.utils import redirect

app = Flask(__name__)
app.config['TESTING'] = True

# 一次更新多个配置值可以使用dict.update()方法
app.config.update(
    TESTING = True,
    SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'
)


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

"""
with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))
"""
if __name__ == '__main__':
    app.run()
