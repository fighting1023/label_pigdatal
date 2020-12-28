# -*- coding: utf-8 -*-
from flask import Flask, g, request
from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key here'
auth = HTTPTokenAuth(scheme='Bearer')
# 实例化一个签名序列化对象 serializer，有效期 10 分钟
serializer = Serializer(app.config['SECRET_KEY'], expires_in=600)
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


# 对视图进行认证
@app.route('/')
@auth.login_required
def index():
    return "Hello, %s!" % g.user



@app.route('/get_uid', methods=['POST'])
@auth.login_required
def get_uid():
    name = request.form['name']

    return "Hello, %s!" % g.user + str(info_dict[name])
info_dict = {"li":1}
if __name__ == '__main__':
    app.run()

"""
curl -X GET -H "Authorization: Token eyJhbGciOiJIUzUxMiIsImlhdCI6MTYwODc5MDM3NCwiZXhwIjoxNjA4NzkwOTc0fQ.eyJ1c2VybmFtZSI6ImpvaG4ifQ.6J1scvVjEvDvlXuAeBoqrDbfFDSxh_q6flt2bqUpEoQlc8HOMxyxI4lUJs1DqTajz8S_E-lFWSBa9JekmXLYFQ" http://localhost:5000/

"""
