from flask import Blueprint, render_template, request, url_for, session, current_app
from app.models import *

login = Blueprint('login', __name__)

@login.route('/index')
def index():
    return render_template('login/index.html')


@login.route('/login', methods=['POST'])
def onlogin():
    '''
    登录
    :return:
    '''
    username = request.json['username']
    password = request.json['password']

    # 判断用户名和密码是否填写
    if not all([username, password]):
        msg = '用户名和密码不能为空'
        return msg

    # 核对用户名和密码是否一致
    user = Users.query.filter_by(username=username, password=password).first()
    # 如果用户名和密码一致
    if user:
        # 向session中写入相应的数据
        session['user_id'] = user.user_id
        session['username'] = user.username
        msg = '1'
        return msg
    # 如果用户名或者密码不一致，则返回并提示
    else:
        msg = '用户名或者密码不一致'
        return msg


@login.route('/register')
def onregister():
    pass
