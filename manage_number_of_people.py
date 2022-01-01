import serial
import time
from multiprocessing import Process, Value, Queue, Array
from serial.tools import list_ports
import datetime as dt
import database_sql


class tmp_database:
    """一日毎のデータを管理"""

    def __init__(self):
        self.people_num_dict = {'now_people':Value('i', 0), 'max_people':Value('i', 0),
                                'total_people':Value('i', 0), 'count_warning':Value('i', 0)}
        
        self.people_num_list_dict = {'max_people_list':Array('i', 9), 'total_people_list':Array('i', 9),
                                     'count_warning_list':Array('i', 9)}
        self.signal_list = Queue()
        

    def increment_people_num(self, variable:str):
        self.people_num_dict[variable].value += 1
    
    def decrement_people_num(self, variable:str):
        self.people_num_dict[variable].value -= 1
    
    def substitution_people_num(self, variable:str, value:int):
        self.people_num_dict[variable].value = value
    
    def append_people_num_list(self, variable:str, var_list:str, index:int):
        if index <= 8:
            print(f'append:{self.people_num_dict[variable].value}')
            self.people_num_list_dict[var_list][index] = self.people_num_dict[variable].value
        else:
            print('index_error')
    
    def initialize_people_num(self, value:int):
        for key in self.people_num_dict.keys():
            self.people_num_dict[key].value = value
    
    def show(self):
        for key in self.people_num_dict.keys():
            print(f'{key}:{self.people_num_dict[key].value}')
        for key in self.people_num_list_dict.keys():
            for i in range(9):
                print(f'{key}[{i}]:{self.people_num_list_dict[key][i]}')
    
    def put(self, variable):
        self.signal_list.put(variable)
    
    def get(self) -> str:
        try:
            rec = self.signal_list.get(block=False)
        except:
            return None
        return rec
    
    def getter(self, variable:str):
        return self.people_num_dict[variable].value


#serialオブジェクトはpickle化不可能、メインプロセスで実行
#tmp_database更新関数を独立させ、pickle化可能にする
class serial_transmission:
    """シリアル通信を行う"""
    def __init__(self, baudrate:int=115200):
        self.isOpen = True
        self.isWarn = False
        self.ser = serial.Serial()
        self.ser.baudrate = baudrate
        self.ser.timeout = 0.1
        devices = [info.device for info in list_ports.comports()]
        if len(devices) == 0:
            print('エラー:ポートが見つかりませんでした')
            self.isOpen = False
        elif len(devices) == 1:
            print(f'ポートが1つ見つかりました{devices[0]}')
            self.ser.port = devices[0]
        else:
            for i in range(len(devices)):
                print(f"input {i:d} open {devices[i]}")
            num = int(input("ポート番号を入力してください:" ))
            self.ser.port = devices[num]
        
        if self.isOpen:
            try:
                self.ser.open()
            except:
                print('ポートが開けませんでした')
                self.isOpen = False
    
    def send(self, string:str):
        self.ser.write(string.encode('ascii'))
    
    def receive(self) -> str:
        rec = self.ser.read().decode('UTF-8')
        return rec
    
    def close(self):
        self.ser.close()
        self.isOpen = False
    
    def predict_and_warn(self, sql:database_sql, index:int,
                         alert:int, max:int, enter:int):
        data = sql.get_data(index)
        if data.alert > alert:
            self.send('w')
        elif data.max_in_room > max:
            self.send('w')
        elif data.enter > enter:
            self.send('w')
    
#並列に扱うため、tmp_databaseのインスタンスを引数にとる
    def keep_waiting_signal(self, end_time:int,
                            tmp_data:tmp_database, standard:int,
                            sql:database_sql, isExistSql = False):
        self.send('d')
        func_time = dt.datetime.now().hour
        while (now := dt.datetime.now().hour) < end_time:
            if (rec := self.receive()) == '':
                pass
            else:
                print(rec)
                tmp_data.put(rec)
                if rec == 'q':
                    print('break_waiting')
                    return False
            if tmp_data.getter('now_people') > standard and not self.isWarn:
                self.send('w')
                self.isWarn = True
                tmp_data.increment_people_num('count_warning')
            elif tmp_data.getter('now_people') <= standard and self.isWarn:
                self.send('s')
                self.isWarn = False
            #sqlDBから値を取得、基準以上なら事前に警告を行うコード
            if isExistSql and now - func_time > 0:
                self.predict_and_warn(sql, 0, 3, 50, 100)
                func_time += 1
        self.send('e')
        return True

#pickle化できないため、分割
class manage_number_of_people:
    def __init__(self):
        self.isFAULT = False
    
#並列に扱うため、tmp_databaseのインスタンスを引数にとる
    def renew_tmp_database(self, end_time:int,
                           standard_time:int, tmp_data:tmp_database):
        func_start_time = dt.datetime.now().hour
        index = 0

        while (hour := dt.datetime.now().hour) < end_time:
            if (signal := tmp_data.get()) is None:
                continue
            if signal == 'i':
                tmp_data.increment_people_num('now_people')
                tmp_data.increment_people_num('total_people')
            elif signal == 'o':
                tmp_data.decrement_people_num('now_people')
            elif signal == 'q':
                print('break_renew')
                break
            else:
                print('予期しない値がリストに格納されていました')
                pass
            if (now := tmp_data.getter('now_people')) > tmp_data.getter('max_people'):
                tmp_data.substitution_people_num('max_people', now)
            if hour - func_start_time >= standard_time:
                func_start_time = dt.datetime().now().hour
                tmp_data.append_people_num_list('max_people', 'max_people_list', index)
                tmp_data.append_people_num_list('total_people', 'total_people_list', index)
                tmp_data.append_people_num_list('count_warning', 'count_warning_list', index)
                tmp_data.substitution_people_num('max_people', 0)
                tmp_data.substitution_people_num('total_people', 0)
                tmp_data.substitution_people_num('count_warning', 0)
                index += 1


if __name__ == '__main__':
    print('start')
    s=manage_number_of_people()
    m=serial_transmission()
    tmp=tmp_database()
    tmp.show()
    start=time.time()
    #シリアル通信はメインプロセスで実行
    p1=Process(target=s.renew_tmp_database, args=(17,1,tmp))
    p1.start()
    isInterrupt = m.keep_waiting_signal(17,tmp,10)
    p1.join()
    print('ok')
    print(time.time()-start)
    tmp.show()
    m.close()