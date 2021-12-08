import datetime
import manage_number_of_people
import schedule
import time
import serial
import database_sql

starttime=8
endtime=17
standard=50

def warn(): #シリアル通信
      ser = serial.Serial("COM11", 9600)    #適当なポート番号
      ser.write("warning")
      ser.close()

def reset(): #人数リセット
    manage_number_of_people.max_people=0
    database_sql.total_people_list[date.how-1]=0
    database_sql.count_warning_list[date.how-1]=0


date=datetime.datetime.now()#現在時刻を取得

while date<endtime: #終了時間まで
    date=datetime.datetime.now() #現在時刻を取得

    if manage_number_of_people.now_people>manage_number_of_people.max_people: #最大人数の更新
        manage_number_of_people.max_people=manage_number_of_people.now_people
    if manage_number_of_people.now_people>standard: #基準以上
        database_sql.count_warning_list[date.how]+=1
        warn()
    if now_time-starttime==1: #一時間経過
        database_sql.max_people_list[date.how-1]=manage_number_of_people.max_people
        add_datas(database_sql.total_people_list[date.how-1],database_sql.max_people_list[date.how-1],database_sql.count_warning_list[date.how-1])
        reset()
        if database_sql.max_people_list[date.how]>50 or database_sql.count_warning_list[date.how]>5 :
            warn()
        starttime=datetime.datetime.now() #開始時刻を更新
