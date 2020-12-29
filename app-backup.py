# -*- coding: utf-8 -*-
from flask import Flask, g, request
from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key here'
auth = HTTPTokenAuth(scheme='Bearer')
# 实例化一个签名序列化对象 serializer，有效期 5 小时 = 18000秒
serializer = Serializer(app.config['SECRET_KEY'], expires_in=18000)
users = ['john', 'susan']
# 生成 token
for user in users:
    token = serializer.dumps({'username': user})
    print('Token for {}: {}\n'.format(user, token))


# 回调函数，对 token 进行验证
@auth.verify_token
def verify_token(token):
    g.user = None
    try:
        data = serializer.loads(token)
    except:
        return False
    if 'username' in data:
        g.user = data['username']
        return True
    return False


@app.route('/api/user_register', methods=['POST'])
def user():
    """用户注册"""
    # 所需参数：name,pwd,tel,realname,add_dtime


# parem_name_list = ["pwd", "tel", "realname"]  # 手机号作为用户名
# parem_value_list = get_param(parem_name_list)  # 接收参数
# dtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# # 判断参数是否有效传递
# if parem_value_list == param_error:
#     return resultmsg(400, parem_value_list, '', '')
# else:
#     # 检查该手机号是否已经注册，以手机号为唯一标识
#     sql_query_all_tel = 'select tel from user'
#     result_query_all_tel = db_execute(sql_query_all_tel)
#     if result_query_all_tel == db_excute_error:
#         resultmsg(500, '用户注册失败', '', '')
#     all_exist_tel = [result_query_all_tel[i][0] for i in range(len(result_query_all_tel))]
#     if parem_value_list[1] in all_exist_tel:
#         return resultmsg(400, '该手机号已注册！', '', '')
#     sql_register_user = 'insert into user (pwd, tel, realname, add_dtime) values ("%s", "%s", "%s", "%s")' \
#                         % (parem_value_list[0], parem_value_list[1], parem_value_list[2], dtime)
#     result = db_execute(sql_register_user)
#     if result == db_excute_error:
#         resultmsg(500, '用户注册失败', '', '')
#     else:
#         return resultmsg(200, '用户注册成功！', '', '')


# 对视图进行认证
@app.route('/')
@auth.login_required
def index():
    token = serializer.dumps({'username': user})
    return "Hello, %s!" % g.user


@app.route('/get_uid', methods=['POST'])
@auth.login_required
def get_uid():
    name = request.form['name']

    return "Hello, %s!" % g.user + str(info_dict[name])


info_dict = {"li": 1}
if __name__ == '__main__':
    app.run()

"""
curl -X GET -H "Authorization: Token eyJhbGciOiJIUzUxMiIsImlhdCI6MTYwODc5MDM3NCwiZXhwIjoxNjA4NzkwOTc0fQ.eyJ1c2VybmFtZSI6ImpvaG4ifQ.6J1scvVjEvDvlXuAeBoqrDbfFDSxh_q6flt2bqUpEoQlc8HOMxyxI4lUJs1DqTajz8S_E-lFWSBa9JekmXLYFQ" http://localhost:5000/

"""
