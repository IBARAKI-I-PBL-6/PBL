import datetime
import database1    //仮のデータベースからのインポート
import schedule
import time
import serial

def reset():  //初期化
  date=0
  for i range(1,25)
    warnhour[i]=0
    data[i]=0

def warn(): //警告カウント、シリアル通信
      database1.warncnt[date.how]++
      database1.warncnthour++
      ser = serial.Serial("COM11", 9600)    //適当なポート番号
      ser.write('1')
      ser.close()

//初期化
reset()

date=datetime.datetime.now()//現在時刻を取得
while date<endtime: //終了時間まで
    date=datetime.datetime.now()
    data[date.how]=database1.data
    if database1.data>10: //適当な人数
        warn()
    if now_time-starttime==1:
        if database1.warncnthour>10 || database1.warncnt[date.how] : //適当
            warn()
        starttime=datetime.datetime.now()
