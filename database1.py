import datetime
import database1
import schedule
import time
import serial

def reset():  //初期化
  date=0
  for i range(1,25)
    warnhour[i]=0
    data[i]=0

def warn(): //警告カウント、シリアル通信
      warnhour[date.how]++
      ser = serial.Serial("COM11", 9600)
      ser.write('1')
      ser.close()

def job:  //main
  date=datetime.datetime.now()
  data[date.how]=database1.data
  if database1.data>10:
    warn()

reset()
//1時間おきに実行
schedule.every().hour.do(job)
