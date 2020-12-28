# -*- coding:utf-8 -*-
import pymysql

pymysql.install_as_MySQLdb()

sql1_create_table_data_label = 'create table data_label (' + \
                               'id int primary key auto_increment, ' + \
                               'dtime datetime(3), ' + \
                               'x_axis float ,' + \
                               'y_axis float , ' + \
                               'z_axis float , ' + \
                               'temp float , ' + \
                               'mac varchar(64), ' + \
                               'ear_side int, ' + \
                               'birthday datetime, ' + \
                               'gender int, ' + \
                               'usbmt_id int);'

sql2_create_table_feature = 'create table feature (' + \
                            'id int primary key auto_increment, ' + \
                            'time_span int' + \
                            'time_rate float ,' + \
                            'usbmt_id int);'

sql3_create_table_pig_info = 'create table pig_info (' + \
                             'id int primary key auto_increment, ' + \
                             'location varchar(64), ' + \
                             'color varchar(32),' + \
                             'mac varchar(64),' + \
                             'birthday datetime,' + \
                             'ear_side int,' + \
                             'gender int);'

sql4_create_table_sensor_data = 'create table sensor_data (' + \
                                'id int primary key auto_increment, ' + \
                                'timestamp bigint, ' + \
                                'dtime datetime(3),' + \
                                'x_axis float, ' + \
                                'y_axis float,' + \
                                'z_axis float,' + \
                                'mac varchar(64), ' + \
                                'temp float);'

sql5_create_table_usbmt = 'create table usbmt (' + \
                          'id int primary key auto_increment, ' + \
                          'mac varchar(64), ' + \
                          'stime datetime(3),' + \
                          'etime datetime(3),' + \
                          'stime_id int,' + \
                          'etime_id int,' + \
                          'label int,' + \
                          'day_age int,' + \
                          'ear_side int,' + \
                          'add_dtime datetime,' + \
                          'add_user_id int );'

sql6_create_table_user = 'create table user (' + \
                         'id BIGINT primary key auto_increment, ' + \
                         'tel varchar(32), ' + \
                         'pwd varchar(64), ' + \
                         'realname varchar(32), ' + \
                         'add_dtime datetime, ' + \
                         'del_tag int, ' + \
                         'del_dtime datetime, ' + \
                         'del_by_id int);'

""" 以下是使用sqlalchemy创建数据库表单，由于未知原因执行错误，只做代码暂留，不使用 """
# # # 配置数据库
# # app = Flask(__name__)
# # # app.config["SQLALCHEMY_DATABASE_URI"] = \
# # #     "mysql://store_manager:store_manager@47.105.91.77:3306/store_management"
# # # app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://li:Naruto123.@47.105.91.77:3306/store_management"
# # app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://%s:%s@%s:%d/%s"%(DBuser, DBpassword, DBhost, DBport, DBdb)
# # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# # app.config['SECRET_KEY'] = 'fljasdfasdf_1._$'
# # app.config["SQLALCHEMY_ECHO"] = True  # 打印sql语句
# #
# # db = SQLAlchemy(app)  # 实例化db
# # print("db:", db)
#
#
# # 创建表
# class User(db.Model):
#     """用户表，存储标注员的个人信息"""
#     __tablename__ = 'user'
#     id = db.Column(db.Integer, primary_key=True)  # 设置为整型之后，primary是自增的，故不用设置自增
#     # name = db.Column(db.String(64))  # 用户名
#     tel = db.Column(db.String(11))  # 联系电话
#     pwd = db.Column(db.String(256))  # 密码
#     power = db.Column(db.String(15))  # 权限
#     realname = db.Column(db.String(64))  # 真实姓名
#     add_dtime = db.Column(db.DateTime)  # 注册时间
#     del_tag = db.Column(db.String(15))  # 删除标记
#     del_dtime = db.Column(db.DateTime(0))  # 删除时间
#     del_user_id = db.Column(db.Integer)  # 删除用户操作的
#
#
# class User_Submit(db.Model):
#     """用户标注表，存储用户提交的数据标注信息，同时可将特征数据放在这里"""
#     __tablename__ = 'usbmt'
#     id = db.Column(db.Integer, primary_key=True)
#     mac = db.Column(db.String(32))  # mac地址
#     stime = db.Column(db.String(32))  # start_time,起始的时间戳或时间值
#     etime = db.Column(db.String(32))  # end_time,结束的时间戳或时间值
#     stime_id = db.Column(db.Integer)  # stime对应的id
#     etime_id = db.Column(db.Integer)  # etime对应的id
#     lable = db.Column(db.Integer)  # 动作对应的标记
#     day_age = db.Column(db.Integer)  # 日龄
#     ear_side = db.Column(db.Integer)  # 耳位
#     add_dtime = db.Column(db.DateTime)  # xxxx-xx-xx xx-xx-xx
#     add_user_id = db.Column(db.Integer)
#
#
# class Data_Label(db.Model):
#     """三轴数据、温度 及 标签、用户提交时的id"""
#     __tablename__ = 'data_label'
#     id = db.Column(db.Integer, primary_key=True)
#     x_axis = db.Column(db.Float)
#     y_axis = db.Column(db.Float)
#     z_axis = db.Column(db.Float)
#     temp = db.Column(db.Float)  # 体温
#     ear_side = db.Column(db.Float)  # 耳标佩戴的位置（左耳：0，右耳：1）
#     usbmt_id = db.Column(db.Integer)  # 用户提交时的id(用于区分同一label的不同个动作)
#
#
# class Sensor_Data(db.Model):
#     """传感器采集到的数据"""
#     __tablename__ = 'sensor_data'
#     id = db.Column(db.Integer, primary_key=True)
#     timestamp = db.Column(db.BIGINT)  # 时间戳
#     dtime = db.Column(db.DateTime(3))  # xxxx-xx-xx xx-xx-xx.xxx
#     x_axis = db.Column(db.Float)
#     y_axis = db.Column(db.Float)
#     z_axis = db.Column(db.Float)
#     temp = db.Column(db.Float)  # 体温
#     mac = db.Column(db.String(32))  # mac地址
#
#
# class Pig_Info(db.Model):
#     """生猪的信息，主要是获取 日龄、耳位"""
#     __tablename__ = 'pig_info'
#     id = db.Column(db.Integer, primary_key=True)
#     position = db.Column(db.String(64))  # 所在猪舍
#     color = db.Column(db.String(32))  # 标记色
#     mac = db.Column(db.String(32))  # mac地址
#     birthday = db.Column(db.DateTime)  # 生日
#     ear_side = db.Column(db.Integer)  # 耳位
#     gender = db.Column(db.Integer)  # 性别
#
#
# class Feature(db.Model):
#     """特征,暂时写在--生猪动作分类.md 文件中"""
#     id = db.Column(db.Integer, primary_key=True)
#     usbmt_id = db.Column(db.Integer)
#
#
# """MySQL建表语句"""
# # if __name__ == '__main__':
# #     db.create_all()
# #     # db.drop_all()  # 删掉数据库中的全部表
