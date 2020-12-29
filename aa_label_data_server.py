from flask import Flask, jsonify
from ad_config import get_param,param_error, app, db_execute, db_execute_error, \
                        resultmsg, int2datetime, serializer, auth, g
import pandas as pd
import time
from ac_create_tables import sql1_create_table_data_label, sql2_create_table_feature, sql3_create_table_pig_info, \
    sql4_create_table_sensor_data, sql5_create_table_usbmt, sql6_create_table_user
# from config import app, db_execute, resultmsg, int2datetime
from collections import defaultdict, OrderedDict
import json
import os
import math
import datetime
import jwt
# from decorators_token import parse_token
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# def get_token(username):
#     token_dict = {'iat': int(time.time()),  # token的生成时间
#                   'username': username,  # 自定义参数，用户名
#                   'exp': int(time.time()) + 20000  # token的有效截至时间
#                   }
#     headers = {'alg': "HS256"}
#     jwt_token = jwt.encode(token_dict,
#                           "zkjy_label_data_platform123",
#                           algorithm='HS256',
#                           headers=headers
#                           ).decode('ascii')
#     return jwt_token


# # 定义解析token
# def parse_token():
#     data = 'token 错误！'
#     try:
#         token = request.form['token']
#         data = jwt.decode(token, 'zkjy_label_data_platform123', algorithms=['HS256'])
#         return data
#     except:
#         return data

# def decorator_parse_token(func):
#     def new_func():
#         token_info = parse_token()
#         if token_info == 'token 错误！':
#             return token_info
#         else:
#             return func()

#     return new_func

# # 处理跨域请求
# app = Flask(__name__)
# CORS(app, supports_credentials=True)
#
# # 配置token
# app.config['SECRET_KEY'] = 'secret key here'
# auth = HTTPTokenAuth(scheme='Bearer')
#
# # 实例化一个签名序列化对象 serializer，有效期 5小时 = 18000秒
# serializer = Serializer(app.config['SECRET_KEY'], expires_in=18000)

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


# 数据库表单创建
@app.route('/api/create_tables', methods=['POST'])
def create_tables():
    param_values_list = get_param(['name', 'pwd'])
    if (not param_values_list[0] == 'li') or (not param_values_list[1] == '123456'):
        return resultmsg(401, '建表独立账号密码错误！', '', '')
    """创建数据库表"""
    result_sql1 = db_execute(sql1_create_table_data_label)
    result_sql2 = db_execute(sql2_create_table_feature)
    result_sql3 = db_execute(sql3_create_table_pig_info)
    result_sql4 = db_execute(sql4_create_table_sensor_data)
    result_sql5 = db_execute(sql5_create_table_usbmt)
    result_sql6 = db_execute(sql6_create_table_user)
    if result_sql1 == db_excute_error or result_sql2 == db_excute_error or result_sql3 == db_excute_error \
            or result_sql4 == db_excute_error or result_sql5 == db_excute_error or result_sql6 == db_excute_error:
        return resultmsg(500, 'Tables creation failed!', '', '')  # 表单创建失败
    else:
        return resultmsg(200, 'Tables creation successful!', '', '')  # 表单创建成功


# 数据库表单删除
@app.route('/api/drop_tables', methods=['POST'])
def drop_tables():
    param_values_list = get_param(['name', 'pwd'])
    if (not param_values_list[0] == 'li') or (not param_values_list[1] == '123456'):
        return resultmsg(401, '建表独立账号密码错误！', '', '')
    result_sql = db_execute('drop table data_label, feature, pig_info, sensor_data, usbmt, user')
    if result_sql == db_excute_error:
        return resultmsg(500, 'Tables deletion failed!', '', '')  # 表单删除失败
    else:
        return resultmsg(200, 'Tables deletion successful!', '', '')  # 表单删除失败


# 1. 用户注册
@app.route('/api/user_register', methods=['POST'])
def user_register():
    """用户注册"""
    # 所需参数，name,pwd,tel,realname,add_dtime
    param_name_list = ["pwd", "tel", "realname"]  # 手机号作为用户名
    param_value_list = get_param(param_name_list)  # 接收参数
    add_dtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # 判断参数是否有效传递
    if param_value_list == param_error:
        return resultmsg(400, param_value_list, '', '')
    else:
        # 对密码进行哈希加密
        param_value_list[0] = generate_password_hash(param_value_list[0])

        # 检查该手机号是否已经注册，以手机号为唯一标识
        sql_count_same_tel = 'select count(*) from user where tel="%s"'%param_value_list[1]
        result_count_same_tel = db_execute(sql_count_same_tel)
        # print('result_count_same_tel:', result_count_same_tel[0][0])
        if result_count_same_tel == db_excute_error:  # sql语句执行失败
            resultmsg(500, '用户注册失败', '', '')
        elif result_count_same_tel[0][0] > 0:
            return resultmsg(401, '该手机号已注册！', '', '')
        else:
            sql_register_user = 'insert into user (pwd, tel, realname, add_dtime) values ("%s", "%s", "%s", "%s")' \
                                % (param_value_list[0], param_value_list[1], param_value_list[2], add_dtime)
            result = db_execute(sql_register_user)
            print(sql_register_user)
            if result == db_excute_error:
                return resultmsg(500, '用户注册失败', '', '')
            else:
                return resultmsg(200, '用户注册成功！', '', '')


# 2. 用户登陆
@app.route('/api/user_login', methods=['POST'])
def user_login():
    """用户登陆"""
    param_name_list = ['tel', 'pwd']
    param_values_list = get_param(param_name_list)
    if param_values_list == param_error:
        return resultmsg(401, param_error, '', '')  # 前端传递的参数值错误

    # 验证手机号和密码
    sql_query_pwd_id = 'select pwd, id from user where tel = "%s"' % param_values_list[0]
    result_query_pwd_id = db_execute(sql_query_pwd_id)
    if result_query_pwd_id == db_excute_error:
        return resultmsg(500, '服务器查询失败，请重试！', '', '')
    result_query_pwd = result_query_pwd_id[0][0]
    result_query_id = result_query_pwd_id[0][1]
    # for i in range(len(result_query_tel_pwd)):
    # 验证密码的正确性
    if check_password_hash(result_query_pwd, param_values_list[1]):
        # return resultmsg(401, '手机号或密码错误！', '', '')
        token = serializer.dumps({'username': param_values_list[0]})
        return resultmsg(200, '登陆成功！',
                         {'user_id': result_query_id, 'tel': param_values_list[0], 'token': str(token)}, '')
    else:
        return resultmsg(401, '手机号或密码错误！', '', '')


# 3. 将xlsx中的数据导入mysql
@app.route('/api/loadxlsx', methods=['GET'])
@auth.login_required
def loadxlsx():
    """上传xlsx数据 三轴数据、体温  按照1秒10条的速度来说，1天的数据量=864000 """
    path = 'DC2E2E15316C_2019-08-19.xlsx'
    df = pd.read_excel(path)
    timestamp = list(df.unix_timestamp)  # <class 'int'>
    # dtime = list(df.date_time)  # <class 'str'>
    x_axis = list(df.x_axis)  # <class 'float'>
    y_axis = list(df.y_axis)  # <class 'float'>
    z_axis = list(df.z_axis)  # <class 'float'>
    temp = list(df.temp)  # <class 'float'>
    mac = list(df.mac)  # <class 'str'>
    insert_value = []
    insert_escape_character = ''
    for i in range(len(timestamp)):
        if i != 0:
            insert_escape_character += ','
        insert_escape_character += '("%s","%s",%.3f,%.3f,%.3f,%.3f,"%s")'
        insert_value += [int(timestamp[i]), str(int2datetime(timestamp[i]))[:-2], x_axis[i], y_axis[i], z_axis[i],
                         temp[i], str(mac[i])]
    sql_insert_sensor_data = 'insert into sensor_data (timestamp, dtime, x_axis, y_axis, z_axis, temp, mac) ' \
                             'values ' + insert_escape_character % tuple(insert_value)
    # print(sql_insert_sensor_data)
    result_insert_sensor_data = db_execute(sql_insert_sensor_data)
    if result_insert_sensor_data == db_excute_error:
        return resultmsg(500, 'sensor_data插入失败！', '', '')
    return resultmsg('数据插入完成！', 200, '', '')


# 4. 根据video_name，请求数据
@app.route('/api/request_data', methods=['POST'])
@auth.login_required
def request_data_test():
    """测试--从csv文件中获取数据"""
    # DC2E2E15316C_2019-08-19 21:13:10_2019-08-19 22:14:45    ABCDEF_BCDEFG_DC2E2E15316C_2019-08-17 183915.100--2019-08-17 195050.mp4
    param_name_list = ['video_name', 'mac']  # DC2E2E15316C_2019-08-17 18:39:15.100_2019-08-17 19:50:50
    param_value_list = get_param(param_name_list)
    if param_value_list == param_error:
        return resultmsg(400, '输入错误，请确认后提交！', '', '')
    """
    这里要对视频名称的正确性做验证
        1. 待查时间范围是否有效
        2. 这几个mac地址是否在同一猪栏内
    """
    macs_in_video_name = param_value_list[0].split("_")[:-1]  # 不要最后一个是起止时间
    mac_ = param_value_list[1]
    setime = param_value_list[0].split("_")[-1][:-4].split("--")  # 不要最后的视频名称后缀.mp4
    stime = setime[0][:13] + ':' + setime[0][13:15] + ':' + setime[0][15:]
    etime = setime[1][:13] + ':' + setime[1][13:15] + ':' + setime[1][15:]
    csv_path = './' + str(mac_) + '/' + str(mac_) + '_' + str(stime)[:10] + '.csv'
    csv_df = pd.read_csv(csv_path)
    query_csv_result = csv_df[(stime < csv_df['dtime']) & (csv_df['dtime'] < etime) & (csv_df['mac'] == mac_)]
    if "Empty DataFrame" in str(query_csv_result):
        return resultmsg(500, '您查询的数据为空，请确认视频名称是否正确！', '', '')
    mac = list(query_csv_result.mac)
    timestamp = list(query_csv_result.timestamp)
    dtime = list(query_csv_result.dtime)
    acc = list(query_csv_result.acc)
    mac = list(query_csv_result.mac)
    # print('len(mac):', len(mac))

    sensor_data = []
    for i in range(len(mac)):
        if len(str(dtime[i])) < 20:
            dtime[i] = str(dtime[i]) + '.000000'
        sensor_data.append({
            "name": dtime[i][:-3],
            "value": [dtime[i][:-3], round(float(acc[i]), 3)],
            "timestamp": timestamp[i],
            "dtime": dtime[i][:-5],
            "acc": round(float(acc[i]), 3),
            "mac": mac[i]
        })
    infodata = {"mac": mac_, "color": "yellow", "position": "1-2-3-4"}  # blue  green
    return resultmsg(200, '数据查询成功！', sensor_data, infodata)


# 5. 用户提交的标注数据
@app.route('/api/label_data', methods=['POST'])
@auth.login_required
def label_data():
    """用户将标注信息提交后，将这个信息存储至usbmt，同时查询原始数+usbmt_id写入data_label"""
    param_name_list = ['mac', 'stime', 'etime', 'label', 'add_user_id']
    param_value_list = get_param(param_name_list)
    if param_value_list == param_error:
        return resultmsg(400, '数据提交错误，请确认后提交！', '', '')
    dtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql_insert_usbmt = 'insert into usbmt (mac, stime, etime, label, add_dtime, add_user_id) values ("%s", "%s", "%s", %d, "%s", %d)' % (
        param_value_list[0], param_value_list[1], param_value_list[2], int(param_value_list[3]), dtime,
        int(param_value_list[4]))
    result_insert_usbmt = db_execute(sql_insert_usbmt)
    last_id = db_execute('select max(id) from usbmt;')[0][0]
    # 利用上传数据的信息，查询到原数据
    csv_path = './' + str(param_value_list[0]) + '/' + str(param_value_list[0]) + '_' + str(param_value_list[1])[
                                                                                        :10] + '.csv'  # 'DC2E2E15316C_2019-08-17.csv'
    csv_df = pd.read_csv(csv_path)
    query_csv_result = csv_df[(param_value_list[1] < csv_df['dtime']) & (csv_df['dtime'] < param_value_list[2]) & (
            csv_df['mac'] == param_value_list[0])]
    if "Empty DataFrame" in str(query_csv_result):
        return resultmsg(500, '您查询的数据为空，请确认视频名称是否正确！', '', '')
    timestamp = list(query_csv_result.timestamp)
    dtime = list(query_csv_result.dtime)
    x_axis = list(query_csv_result.x_axis)
    y_axis = list(query_csv_result.y_axis)
    z_axis = list(query_csv_result.z_axis)
    acc = list(query_csv_result.acc)
    mac = list(query_csv_result.mac)
    temp = list(query_csv_result.temp)

    insert_value = []
    insert_escape_character = ' (%d,"%s",%.3f,%.3f,%.3f,%.3f,"%s",%.3f, %d) '
    for i in range(len(timestamp)):
        insert_value += [(int(timestamp[i]), str(dtime[i]), float(x_axis[i]), float(y_axis[i]), float(z_axis[i]),
                          float(acc[i]), str(mac[i]), float(temp[i]), int(last_id))]
    sql_insert_data_label = 'insert into data_label (timestamp, dtime, x_axis, y_axis, z_axis, acc, mac, temp, usbmt_id) values ' + str(
        tuple(insert_value))[1:-1]
    result_insert_data_label = db_execute(sql_insert_data_label)
    if result_insert_data_label == db_excute_error:
        return resultmsg(500, '数据提交发生错误，请重新提交！2', '', '')
    return resultmsg(200, '标注数据提交成功！', '', '')


# 用真实数据写一个json文件
@app.route('/api/write_json', methods=['GET'])
def write_json():
    sql_query_datetime_data = 'select id, timestamp, dtime, x_axis, y_axis, z_axis, mac, temp from sensor_data'
    result_query_datetime_data = db_execute(sql_query_datetime_data)
    if result_query_datetime_data == db_excute_error:
        return resultmsg(500, '数据查询失败，请重试！', '', '')
    path_json = 'sensor_data json/'
    filename_mac = str(result_query_datetime_data[0][6]) + '_'
    filename_stime = str(result_query_datetime_data[0][2]) + '_'
    filename_etime = str(result_query_datetime_data[-1][2]) + '_'
    filename_extension = 'json'
    filename = filename_mac + filename_stime + filename_etime + filename_extension
    if os.path.exists(path_json):
        files_in_path_json = os.listdir(path_json)
        for i in range(len(files_in_path_json)):
            os.remove(os.path.join(path_json, files_in_path_json[i]))
    else:
        os.makedirs(path_json)
    fw = open(filename, 'a', encoding='utf-8')
    for item in range(len(result_query_datetime_data)):
        data_dict = {"id": result_query_datetime_data[item][0],
                     "timestamp": result_query_datetime_data[item][1],
                     "dtime": result_query_datetime_data[item][2],
                     "x_axis": result_query_datetime_data[item][3],
                     "y_axis": result_query_datetime_data[item][4],
                     "z_axis": result_query_datetime_data[item][5],
                     "mac": result_query_datetime_data[item][6],
                     "tenp": result_query_datetime_data[item][7]}
        json.dump(data_dict, fw)
    fw.close()
    return resultmsg(200, 'datetime data', result_query_datetime_data, '')


# 1566038355100
@app.route('/api/tocsv', methods=['GET'])
def tocsv():
    sql_query_sensor_data = 'select * from sensor_data'
    result_query_sensor_data = db_execute(sql_query_sensor_data)

    id = []
    timestamp = []
    dtime = []
    x_axis = []
    y_axis = []
    z_axis = []
    acc = []
    mac = []
    temp = []

    for i in range(len(result_query_sensor_data)):
        id.append(result_query_sensor_data[i][0])
        timestamp.append(result_query_sensor_data[i][1])
        dtime.append(str(result_query_sensor_data[i][2]))
        x_axis.append(result_query_sensor_data[i][3])
        y_axis.append(result_query_sensor_data[i][4])
        z_axis.append(result_query_sensor_data[i][5])
        acc.append(round(math.sqrt(float(x_axis[-1]) ** 2 + float(y_axis[-1]) ** 2 + float(z_axis[-1]) ** 2), 3))
        mac.append(result_query_sensor_data[i][6])
        temp.append(result_query_sensor_data[i][7])

    df = pd.DataFrame(
        {"id": id, "timestamp": timestamp, "dtime": dtime, "x_axis": x_axis, "y_axis": y_axis, "z_axis": z_axis,
         "acc": acc, "mac": mac, "temp": temp})
    df.to_csv(str(mac[-1]) + "_" + str(dtime[0][:10]) + '.csv')
    return resultmsg(200, '已经导出csv文件！', '', '')


# 全局变量


db_excute_error = 'db_excute() error'  # sql语句执行错误的返回值
param_error = 'param error'

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
    # app.run(host='0.0.0.0', port=5000, debug=True)
