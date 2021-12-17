#Tell, don't ask
import serial
import time
from multiprocessing import Process, Value, Manager, Queue
from serial.tools import list_ports


class tmp_database:
    """一日毎のデータを管理"""

    def __init__(self):
        self.manager = Manager()
        self.people_num_dict = {'now_people':self.manager.Value('i', 0), 'max_people':self.manager.Value('i', 0)
                                                                       , 'total_people':self.manager.Value('i', 0)
                                                                       , 'count_warning':self.manager.Value('i', 0)}
        
        self.people_num_list_dict = {'max_people_list':self.manager.list(), 'total_people_list':self.manager.list()
                                                                          , 'count_warning_list':self.manager.list()}
        

    def increment_people_num(self, variable:str):
        self.people_num_dict[variable].value += 1
    
    def decrement_people_num(self, variable:str):
        self.people_num_dict[variable].value -= 1
    
    def substitution_people_num(self, variable:str, value:int):
        self.people_num_dict[variable].value = value
    
    def append_people_num_list(self, variable:str, var_list:str):
        self.people_num_list_dict[var_list].append(self.people_num_dict[variable].value)
    
    def initialize_people_num(self, value:int):
        for key in self.people_num_dict.keys():
            self.people_num_dict[key].value = value
    
    def show(self):
        for key in self.people_num_dict.keys():
            print(f'{key}:{self.people_num_dict[key].value}')


class serial_transmission:
    """シリアル通信を行う"""
    def __init__(self, baudrate:int=115200):
        self.isOpen = True
        self.ser = serial.Serial()
        self.ser.baudrate = baudrate
        self.ser.timeout = None
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

class manage_number_of_people:
    def __init__(self) -> None:
        self.manager = Manager()
        self.signal_list = Queue()
        self._serial = serial_transmission()
        self.tmp_data = tmp_database()
        if not self._serial.isOpen:
            print('シリアル通信に失敗しました')
            return None
    
    def keep_waiting_signal(self, operating_time:int, start_time:float):
        while time.time() - start_time < operating_time:
            rec = self._serial.receive()
            print(rec)
            self.signal_list.put(rec)
    
    def renew_tmp_database(self, operating_time:int, standard_time:int, start_time:float):
        func_start_time = time.time()
        while time.time() - func_start_time < operating_time:
            try:
                signal = self.signal_list.get(block=False)
            except:
                continue
            if signal == 'i':
                self.tmp_data.increment_people_num('now_people')
                self.tmp_data.increment_people_num('total_people')
            elif signal == 'o':
                self.tmp_data.decrement_people_num('now_people')
            else:
                print('予期しない値がリストに格納されていました')
            if time.time() - func_start_time > standard_time:
                func_start_time = time.time()
                self.tem_data.append_people_num_list('max_people', 'max_people_list')
                self.tem_data.append_people_num_list('total_people', 'total_people_list')
                self.tem_data.append_people_num_list('count_warning', 'count_warning_list')

if __name__ == '__main__':
    print('test')
    ope = manage_number_of_people()
    start = time.time()
    print('start')
    if ope is None:
        print('error')        
    else:
        p1=Process(target = ope.keep_waiting_signal, args = (10, start, ))
        p2=Process(target = ope.renew_tmp_database, args = (10, 1000, start, ))
        p1.start()
        p2.start()
        p1.join()
        p2.join()
        ope.tmp_data.show()
        ope._serial.close()