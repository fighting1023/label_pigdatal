import os
import pandas as pd
import time
import datetime


def str_second_datetime2int_10timestamp(str_second_datetime):
    """将字符串型【秒级】格式化时间 转为 【10位】整型时间戳"""
    ans_time_stamp = int(time.mktime(time.strptime(str_second_datetime, "%Y-%m-%d %H:%M:%S")))
    return ans_time_stamp


def int2datetime(int_float_timestamp):
    """
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


"""
,id,timestamp,dtime,x_axis,y_axis,z_axis,acc,mac,temp
0,1,1566038355100,2019-08-17 18:39:15.100000,0.125,0.04,-0.316,0.342,DC2E2E15316C,36.5
"""
timestamp = []
dtime = []
x_axis = []
y_axis = []
z_axis = []
acc = []
mac = []
temp = []

exist_macs = ['AB2E2E15316C', 'CD2E2E15316C', 'EF2E2E15316C', 'GH2E2E15316C']

datetime1 = '2020-12-18 09:20:31'
int_timestamp = int(str_second_datetime2int_10timestamp(datetime1))
formdatetime = int2datetime(int_timestamp)

temp_timestamp = 1607563231000
# while 1607563231000 < temp_timestamp < 1608254431000:
#     if
