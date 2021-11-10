import serial
import datetime

buf = 0                     #入ってきた合計人数
database1_1 = 0             #部屋内の現在の人数
database1_2 = []            #入ってきた合計人数を一時間毎に記録するとこ
time_counter = 0           #database1_2の要素の番号

d_start = datetime.date()   #現在の"年月日時分秒"取得
hour1 = d_start.hour        #"時"のみ抽出
now_time = hour1            #開始時刻に実行時の"時"を入れる
last_time = 18              #終了時刻を設定(任意の数)

while now_time < last_time:
    #現在時刻取得
    d_today = datetime.date()   #現在の"年月日時分秒"取得
    hour2 = d_start.hour        #"時"のみ抽出
    minute = d_today.minute     #"分"のみ抽出
    second = d_today.second     #"秒"のみ抽出

    #シリアル信号受信
    ser = serial.Serial('/dev/tty.', 10000, timeout = None)
    i = ser.readline()
    ser.close()
    #i==1のとき人数増加
    #i==2のとき人数減少

    #人数増減
    if i == 1:
        database1_1 += 1
        buf += 1
    elif i == 2:
        database1_1 -= 1

    if minute==59 && second==59:         #59分59秒
        database1_2[time_counter] = buf  #database1_2に値を保存
        time_counter += 1
        buf = 0                          #bufをリセット

    now_time = hour2                     #現在時刻の更新
