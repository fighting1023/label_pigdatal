# -*- coding: utf-8 -*-
from flask import Flask, g, request
from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from ab_settings import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE
from pymysql import connect
from pymysql.cursors import DictCursor  # 为了返回字典形式的数据

from ac_create_tables import sql1_create_table_data_label, sql2_create_table_feature, sql3_create_table_pig_info,\
                                sql4_create_table_sensor_data, sql5_create_table_usbmt, sql6_create_table_user

db_conn = connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER,
                  password=MYSQL_PASSWORD, database=MYSQL_DATABASE, charset='utf8')
db_cursor = db_conn.cursor(DictCursor)  # 将查询的数据以字典的形式返回

def db_execute_sql(sql):
    data = []
    result = db_cursor.execute(sql)
    print(result)
    return str(result)





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

@app.route('/create_tables', methods=['POST'])
def create_tables():
    if request.form['li123456'] == 'li123456':
        db_execute_sql(sql1_create_table_data_label)
        return 'sql1... 执行成功！'
    return 'sql1... 执行失败！'




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


info_dict = {"li": 1}
if __name__ == '__main__':
    app.run()

"""
curl -X GET -H "Authorization: Token eyJhbGciOiJIUzUxMiIsImlhdCI6MTYwODc5MDM3NCwiZXhwIjoxNjA4NzkwOTc0fQ.eyJ1c2VybmFtZSI6ImpvaG4ifQ.6J1scvVjEvDvlXuAeBoqrDbfFDSxh_q6flt2bqUpEoQlc8HOMxyxI4lUJs1DqTajz8S_E-lFWSBa9JekmXLYFQ" http://localhost:5000/

"""
