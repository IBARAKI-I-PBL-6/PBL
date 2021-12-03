import datetime
import pbl_raspi_in   //仮のデータベースからのインポート
import schedule
import time
import serial

starttime=8
endtime=18
def reset():  //初期化
  date=0
  for i range(1,25)
    warnhour[i]=0
    data[i]=0

def warn(): //シリアル通信
      ser = serial.Serial("COM11", 9600)    //適当なポート番号
      ser.write('1')
      ser.close()

//初期化
reset()

date=datetime.datetime.now()//現在時刻を取得
while date<endtime: //終了時間まで
    date=datetime.datetime.now()
    data[date.how]=pbl_raspi_in.database1_1
    if pbl_raspi_in.database1_1>10: //適当な人数
        database2.warncnt[date.how]++
        database2.warncnthour++
        warn()
    if now_time-starttime==1:
        if database2.warncnthour>10 || database2.warncnt[date.how]>10 : //適当
            warn()
        starttime=datetime.datetime.now()
