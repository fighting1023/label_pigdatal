# -*- coding:utf-8 -*-

from flask import Flask, request, g
from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import pymysql
from flask_cors import CORS
from DBUtils.PersistentDB import PersistentDB
import time, datetime
from ab_settings import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE

pymysql.install_as_MySQLdb()

# 配置数据库
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key here'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://%s:%s@%s:%d/%s" % (MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True  # 打印sql语句
auth = HTTPTokenAuth(scheme='Bearer')

# 实例化一个签名序列化对象 serializer，有效期 5 小时 = 18000秒
serializer = Serializer(app.config['SECRET_KEY'], expires_in=18000)


# 添加进程池
POOL = PersistentDB(
    creator=pymysql,
    maxusage=None,
    setsession=[],  # 开始会话前执行的命令列表.
    ping=1,
    closeable=False,
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE,
    charset='utf8'
)

# 使用进程池连接MySQL
db_conn = POOL.connection()
db_cursor = db_conn.cursor()


# 处理跨域请求
CORS(app, supports_credentials=True)

# @auth.verify_token
# def verify_token(token):
#     g.user = None
#     try:
#         data = serializer.loads(token)
#     except:
#         return False
#     if 'username' in data:
#         g.user = data['username']
#         return True
#     return False


param_error = 'get param error'
def get_param(param_name_list):
    int_list = []  # 需要转为整型的参数列表
    float_list = []  # 需要转为浮点型的参数列表

    param_error = 0
    param_value_list = []
    for i in range(len(param_name_list)):
        param_name = param_name_list[i]  # 拿到参数名称
        try:
            param_value = request.form[str(param_name)]  # 拿到字符型的参数值
            if param_name in int_list:
                param_value_list.append(int(param_value.strip()))  # 转为整型
            elif param_name in float_list:
                param_value_list.append(float(param_value.strip()))  # 转为浮点型
            else:
                param_value_list.append(param_value.strip())  # 去除字符串两侧的空字符
        except:
            param_error = 1  # 参数提取错误
    if param_error == 0:
        return param_value_list
    else:
        return "param error"

db_execute_error = 'db execute error'
def db_execute(sql, conn=db_conn, cursor=db_cursor):
    """
    定义执行sql语句的流程
    """
    try:
        res1 = cursor.execute(sql)
        res2 = conn.commit()
        result = cursor.fetchall()
        return result
    except:
        conn.rollback()
        return 'db_excute() error'


def resultmsg(code, msg, data, pageDetail):
    """定义返回语句标准格式"""
    result = {
        "msg": msg,
        "code": code,
        "data": data,
        "pageDetail": pageDetail
    }
    return result


def int2datetime(int_float_timestamp):
    """
    时间戳转为格式化时间
    有小数点：分离小数点，整数转为格式化时间，小数点直接跟在后面
    无小数点：从第10位进行分离，
    所以本函数只适用于时间戳整数位数大于9且小于11.
    """
    if '.' in str(int_float_timestamp):
        int_float = str(int_float_timestamp).split('.')
        date = time.localtime(int(int_float[0]))
        tempDate = time.strftime("%Y-%m-%d %H:%M:%S", date)
        secondafter = '.' + str(int_float[1])
        return str(tempDate) + secondafter
    else:
        if len(str(int_float_timestamp)) == 10:
            # 精确到秒
            timeValue = time.localtime(int_float_timestamp)
            tempDate = time.strftime("%Y-%m-%d %H:%M:%S", timeValue)
            datetimeValue = datetime.datetime.strptime(tempDate, "%Y-%m-%d %H:%M:%S")
        elif 10 < len(str(int_float_timestamp)) and len(str(int_float_timestamp)) < 15:
            # 精确到毫秒
            k = len(str(int_float_timestamp)) - 10
            timetamp = datetime.datetime.fromtimestamp(int_float_timestamp / (1 * 10 ** k))
            datetimeValue = timetamp.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        elif 14 < len(str(int_float_timestamp)) and len(str(int_float_timestamp)) < 18:
            # 精确到毫秒
            k = len(str(int_float_timestamp)) - 10
            timetamp = datetime.datetime.fromtimestamp(int_float_timestamp / (1 * 10 ** k))
            datetimeValue = timetamp.strftime("%Y-%m-%d %H:%M:%S.%f")
        else:
            return -1
        return datetimeValue
