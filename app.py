# encoding: utf-8

from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask import session
from flask_pymongo import PyMongo
import config

app = Flask(__name__)
app.config.from_object(config)
mongo = PyMongo(app)

@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        user = mongo.db.user.find_one({
            'username': username,
            'password': password
        })
        print username
        print password
        print user
        if user:
            session['user_id'] = user['user_id']
            return redirect(url_for('index'))
        else:
            return u'用户名或密码错误'


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # 验证用户名是否已存在
        if list(mongo.db.user.find({'username': username})):
            return u'该用户名已经注册'
        else:
            # 验证password1与password2相等
            if password1 != password2:
                return u'两次密码不同'
            else:
                user_id_list = [doc['user_id'] for doc in mongo.db.user.find()]
                if user_id_list:
                    max_user_id = max(user_id_list)
                else:
                    max_user_id = 0
                mongo.db.user.insert_one({
                    'user_id': max_user_id + 1,
                    'username': username,
                    'password': password1
                })
                return redirect(url_for('login'))


@app.route('/question', methods=['GET', 'POST'])
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        pass



@app.context_processor
def my_context_processor():
    # 钩子函数，返回的字典在所有页面都可以访问其中的对象
    user_id = session.get('user_id')
    if user_id:
        user = mongo.db.user.find_one({'user_id': user_id})
        return {'user': user}
    else:
        return {}


if __name__ == '__main__':
    app.run()
